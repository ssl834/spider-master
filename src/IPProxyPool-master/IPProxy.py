# coding:utf-8

from multiprocessing import Value, Queue, Process
from db.DataStore import store_data
from validator.Validator import validator, getMyIP
from spider.ProxyCrawl import startProxyCrawl

from config import TASK_QUEUE_SIZE,DB_CONFIG
def main():
    myip = getMyIP()
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM, myip,'FREE'))
    p2 = Process(target=validator, args=(q1, q2, myip,'FREE'))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM,'FREE'))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

if __name__ == "__main__":
    main()

