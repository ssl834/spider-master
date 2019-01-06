# coding:utf-8
import sys

import chardet
from gevent import monkey
monkey.patch_all()

import json
import os
import gevent
import requests
import time
import psutil
from multiprocessing import Process, Queue

import config
from db.DataStore import get_sqlhelper
from util.exception import Test_URL_Fail

# 数据库检测
def detect_from_db(myip, proxy, proxies_set,proxy_type):
    sqlhelper=get_sqlhelper(proxy_type)
    proxy_dict = {'ip': proxy[0], 'port': proxy[1]}
    result = detect_proxy(myip, proxy_dict)
    if result:
        proxy_str = '%s:%s' % (proxy[0], proxy[1])
        proxies_set.add(proxy_str)

    else:
        if proxy[2] < 1:
            sqlhelper.delete({'ip': proxy[0], 'port': proxy[1]})
        else:
            score = proxy[2]-1
            sqlhelper.update({'ip': proxy[0], 'port': proxy[1]}, {'score': score})
            proxy_str = '%s:%s' % (proxy[0], proxy[1])
            proxies_set.add(proxy_str)


# 检测主程序
def validator(queue1, queue2, myip,proxy_type):
    tasklist = []
    proc_pool = {}     # 所有进程列表
    cntl_q = Queue()

    while True:
        if proxy_type !='dedicated':
            if not cntl_q.empty():
                # 处理已结束的进程
                try:
                    pid = cntl_q.get()
                    proc = proc_pool.pop(pid)
                    proc_ps = psutil.Process(pid)
                    proc_ps.kill()
                    proc_ps.wait()
                except Exception as e:
                    pass

            try:
                if len(proc_pool) >= config.MAX_CHECK_PROCESS:
                    time.sleep(config.CHECK_WATI_TIME)
                    continue
                proxy = queue1.get()
                tasklist.append(proxy)
                if len(tasklist) >= config.MAX_CHECK_CONCURRENT_PER_PROCESS:
                    p = Process(target=process_start, args=(tasklist, myip, queue2, cntl_q))
                    p.start()
                    proc_pool[p.pid] = p
                    tasklist = []

            except Exception as e:
                if len(tasklist) > 0:
                    p = Process(target=process_start, args=(tasklist, myip, queue2, cntl_q))
                    p.start()
                    proc_pool[p.pid] = p
                    tasklist = []
        else:
            pass

    #
def process_start(tasks, myip, queue2, cntl):
    spawns = []
    for task in tasks:
        spawns.append(gevent.spawn(detect_proxy, myip, task, queue2))
    gevent.joinall(spawns)
    cntl.put(os.getpid())  # 子进程退出是加入控制队列


def detect_proxy(selfip, proxy, queue2=None):
    '''
    :param proxy: ip字典
    :return:
    '''
    ip = proxy['ip']
    port = proxy['port']
    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
    protocol, types, speed = getattr(sys.modules[__name__],config.CHECK_PROXY['function'])(selfip, proxies)
    if protocol >= 0:
        proxy['protocol'] = protocol
        proxy['types'] = types
        proxy['speed'] = speed
    else:
        proxy = None
    if queue2:
        queue2.put(proxy)
    return proxy


def checkProxy(selfip, proxies):
    '''

    :param
    :return:
    '''
    protocol = -1
    types = -1
    speed = -1
    http, http_types, http_speed = _checkHttpProxy(selfip, proxies)
    https, https_types, https_speed = _checkHttpProxy(selfip, proxies, False)
    if http and https:
        protocol = 2
        types = http_types
        speed = http_speed
    elif http:
        types = http_types
        protocol = 0
        speed = http_speed
    elif https:
        types = https_types
        protocol = 1
        speed = https_speed
    else:
        types = -1
        protocol = -1
        speed = -1
    return protocol, types, speed

# 检测 代理类型
def _checkHttpProxy(selfip, proxies, isHttp=True):
    types = -1
    speed = -1
    if isHttp:
        test_url = config.TEST_HTTP_HEADER
    else:
        test_url = config.TEST_HTTPS_HEADER
    try:
        start = time.time()
        r = requests.get(url=test_url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
        if r.ok:
            speed = round(time.time() - start, 2)
            content = json.loads(r.text)
            headers = content['headers']
            ip = content['origin']
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                types = 2
            elif proxy_connection:
                types = 1
            else:
                types = 0

            return True, types, speed
        else:
            return False, types, speed
    except Exception as e:
        return False, types, speed


def baidu_check(selfip, proxies):
    '''
    :param
    :return:
    '''
    protocol = -1
    types = -1
    speed = -1

    try:
        start = time.time()
        r = requests.get(url='https://www.baidu.com', headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
        if r.ok:
            speed = round(time.time() - start, 2)
            protocol= 0
            types=0

        else:
            speed = -1
            protocol= -1
            types=-1
    except Exception as e:
            speed = -1
            protocol = -1
            types = -1
    return protocol, types, speed

def getMyIP():
    try:
        r = requests.get(url=config.TEST_IP, headers=config.get_header(), timeout=config.TIMEOUT)
        ip = json.loads(r.text)
        return ip['origin']
    except Exception as e:
        raise Test_URL_Fail


if __name__ == '__main__':
    ip = '222.186.161.132'
    port = 3128
    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
    _checkHttpProxy(None,proxies)
