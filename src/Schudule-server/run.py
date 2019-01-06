from tornado.web import RequestHandler,Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define
import tornado,sys,os,requests
from scrapyd_system.utils.utils import printf
from multiprocessing.dummy import Pool as ThreadPool
from scrapyd_system.gathersystem import GatherSystem
def main():
    app=Application([(r'/index',GatherSystem)])
    http_server=HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    IOLoop.current().start()


def check_scrapyd_connectivity(servers):
    printf("Checking connectivity of SCRAPYD_SERVERS")

    def check_connectivity(server):
        (group, ip, port, auth) = server
        try:
            r = requests.get('http://%s:%s' % (ip, port), auth=auth, timeout=3)
            assert r.status_code == 200
        except:
            return False
        else:
            return True
    pool = ThreadPool(min(len(servers), 100))
    results = pool.map(check_connectivity, servers)
    pool.close()
    pool.join()

    print("Index {group:<20} {server:<21} Connectivity Auth".format(
          group='Group', server='Scrapyd IP:Port'))
    print('#' * 100)
    for idx, ((group, ip, port, auth), result) in enumerate(zip(servers, results), 1):
        print("{idx:_<5} {group:_<20} {server:_<22} {result:_<11} {auth}".format(
              idx=idx, group=group or 'None', server='%s:%s' % (ip, port), auth=auth, result=str(result)))
    print('#' * 100)

    if not any(results):
        sys.exit("\n!!! None of your SCRAPYD_SERVERS could be connected.\n")
if __name__ == '__main__':
    main()
