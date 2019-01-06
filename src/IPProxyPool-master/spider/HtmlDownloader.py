# coding:utf-8

import random
import config
import json
from db.DataStore import get_sqlhelper
import requests
import chardet


class Html_Downloader(object):
    @staticmethod
    def download(url,proxy_type):
        try:
            r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)
            r.encoding = chardet.detect(r.content)['encoding']

            if (not r.ok) or len(r.content) < 500:

                raise ConnectionError
            else:

                return r.text

        except Exception:
            count = 0  # 重试次数
            sqlhelper=get_sqlhelper(proxy_type)
            proxylist = sqlhelper.select(10)
            if not proxylist:
                return None
            print(111)

            while count < config.RETRY_TIME:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None
