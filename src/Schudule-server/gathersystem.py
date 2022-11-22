from tornado.web import RequestHandler,Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define
import shutil
define('port',5000)
import os,tornado,requests
import tarfile,zipfile
class GatherSystem(RequestHandler):
    method=['POST',"GET"]
    def initialize(self):
        if self.request.method not in self.method:
            self.write('非法请求方式')
    # 接受文件上传
    def post(self):
        file=self.request.files['aa'][0]
        filename=file['filename']
        filepath=os.getcwd()
        with open(filepath+'/'+filename,'wb')as f:
            f.write(file['body'])
        # 解压上传文件,并获得解压之后的文件路径
        new_path=UnCompress(file,filepath).uncompress()
        if not new_path:
            return '解压失败'
        print(new_path)
        if 'scrapy.cfg' not in os.listdir(new_path):
            # 没有此文件 直接创建并写入参数
            with open(new_path+'/scrapy.cfg', 'w') as f:
                f.write('[settings]\ndefault = {}.settings\n[deploy:{}]\nurl=http://localhost:6800/\nproject={}'.format('Phone','name', "Phone"))
        else:
            #有此文件 检测此文件参数是否符合需要
            pass
        os.system('cd {} && scrapyd-deploy {} -p {}'.format(new_path,'name','Phone'))
        resq=requests.get('http://localhost:6800/daemonstatus.json')
        print(resq.text)


    # 检测文件是否规范，如果不规范重新写入
    def check_scrapy_cfg(self,new_path):
        ls=os.listdir(new_path)
        for i in ls:
            c_path = os.path.join(new_path, i)
            if os.path.isdir(c_path):
                self.check_scrapy_cfg(c_path)
            elif os.path.isfile(c_path):
                print(1111)
                if 'scrapy.cfg'==i:
                    print(2222)
                    with open(i,'r') as f:
                        f.read()
                else:
                    with open('scrapy.cfg','w') as f:
                        f.write('[deploy:{}]\nurl=localhost:6800/\nproject={}'.format('name',"Phone"))
    #进入文件使用scrapyd部署




class UnCompress(object):
    """解压上传文件"""
    target_path='/home/worker/'
    def __init__(self,file_obj,file_path):

        self.file_obj=file_obj
        self.file_path=file_path
    def uncompress(self):
        file=self.file_obj['filename']
        filename=file.split('.')[0]
        file_suffix=file.split('.')[1]
        if filename not in os.listdir(self.target_path):
            os.mkdir(self.target_path+'{}'.format(filename))
        else:
            print('文件夹已经存在，删除')
            exit_file_path=self.target_path+'{}'.format(filename)
            self.del_exit_file(exit_file_path)
        if 'zip' ==file_suffix:
            new_path=self.target_path+'{}'.format(filename)
            with zipfile.ZipFile(self.file_path+'/{}'.format(self.file_obj['filename']),'r') as f:
                f.extractall(path=new_path)

        elif 'tar'==file_suffix:
            new_path = self.target_path + '{}'.format(filename)
            with tarfile.open(self.file_path+'{}'.format(filename),'r') as f:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(f, path=new_path)
        elif 'egg'==file_suffix:
            new_path=self.target_path+'{}'.format(filename)
            newname=new_path+'{}'.format(file)
            # 复制文件
            shutil.copyfile(self.file_obj['body'],newname)
        else:
            new_path=''
        return new_path

    # 删除已存在的文件夹下的所有文件
    def del_exit_file(self,file_path):
        ls = os.listdir(file_path)
        for i in ls:
            c_path = os.path.join(file_path, i)
            if os.path.isdir(c_path):
                self.del_exit_file(c_path)
            else:
                os.remove(c_path)


app=Application([(r'/index',GatherSystem)])
http_server=HTTPServer(app)
http_server.listen(9000)
IOLoop.current().start()