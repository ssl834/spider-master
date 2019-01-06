# coding:utf-8
from gevent import monkey
monkey.patch_all()

import sys
import time
import gevent

from gevent.pool import Pool
from multiprocessing import Queue, Process, Value


from config import THREADNUM, parserList, UPDATE_TIME, MINNUM, MAX_CHECK_CONCURRENT_PER_PROCESS, MAX_DOWNLOAD_CONCURRENT,PAY_IP_URL
from db.DataStore import store_data, get_sqlhelper
from spider.HtmlDownloader import Html_Downloader
from spider.HtmlPraser import Html_Parser
from validator.Validator import validator, getMyIP, detect_from_db




def startProxyCrawl(queue, db_proxy_num,myip,proxy_type):
    crawl = ProxyCrawl(queue, db_proxy_num,myip,proxy_type)
    crawl.run()


class ProxyCrawl(object):
    """爬虫主程序"""
    proxies = set()

    def __init__(self, queue, db_proxy_num,myip,proxy_type):
        self.crawl_pool = Pool(THREADNUM)
        self.queue = queue
        self.db_proxy_num = db_proxy_num
        self.myip = myip
        self.proxy_type=proxy_type


    def run(self):
        while True:
            self.proxies.clear()
            str = 'IPProxyPool----->>>>>>>>beginning'
            sys.stdout.write(str + "\r\n")
            sys.stdout.flush()
            sqlhelper=get_sqlhelper(self.proxy_type)
            if self.proxy_type.lower()=='free':
                proxylist = sqlhelper.select()

                spawns = []
                for proxy in proxylist:
                    spawns.append(gevent.spawn(detect_from_db, self.myip, proxy, self.proxies))
                    if len(spawns) >= MAX_CHECK_CONCURRENT_PER_PROCESS[self.proxy_type]:
                        gevent.joinall(spawns)
                        spawns= []
                gevent.joinall(spawns)
                self.db_proxy_num.value = len(self.proxies)
                str = 'IPProxyPool----->>>>>>>>db exists ip:%d' % len(self.proxies)

                if len(self.proxies) < MINNUM:
                    str += '\r\nIPProxyPool----->>>>>>>>now ip num < MINNUM,start crawling...'
                    sys.stdout.write(str + "\r\n")
                    sys.stdout.flush()
                    spawns = []
                    if self.proxy_type=='PAY':
                        proxylist=PAY_IP_URL
                    for p in parserList:
                        spawns.append(gevent.spawn(self.crawl, p))

                        if len(spawns) >= MAX_DOWNLOAD_CONCURRENT[self.proxy_type]:
                            gevent.joinall(spawns)
                            spawns= []
                    gevent.joinall(spawns)
                else:
                    str += '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                    sys.stdout.write(str + "\r\n")
                    sys.stdout.flush()

                time.sleep(UPDATE_TIME)




    def crawl(self, parser):

        html_parser = Html_Parser()
        for url in parser['urls']:
            response = Html_Downloader.download(url,self.proxy_type)
            if response is not None:
                proxylist = html_parser.parse(response, parser)

                if proxylist is not None:
                    for proxy in proxylist:
                        proxy_str = '%s:%s' % (proxy['ip'], proxy['port'])
                        if proxy_str not in self.proxies:
                            self.proxies.add(proxy_str)
                            while True:
                                if self.queue.full():
                                    time.sleep(0.1)
                                else:
                                    self.queue.put(proxy)
                                    break




