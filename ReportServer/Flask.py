# coding=utf-8
import os,sys
from flask import Flask, request
from flask import render_template
from werkzeug.utils import secure_filename
from ReportServer import EasyRun
rootpath = str(sys.argv[0]).split('/')
lists = list(rootpath)
del lists[-1]
newpath = '/'.join(lists)
os.chdir(newpath)
print '当前文件路径:'+os.getcwd()



host = '127.0.0.1'
port = 5000

def create_app():
    '''
    创建app
    :return:app
    '''
    app = Flask(__name__)
    return app


app = create_app()
base_dir = os.path.dirname(__file__)
UPLOAD_FOLDER = base_dir + '/TestApp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['apk'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def runflask():
    '''
    启动Flask
    :return:
    '''
    app.run(host=host, port=port, debug=False, threaded=False)
    #app.run(debug=True, threaded=False)


def stopflask():
    '''
    停止Flask
    :return:
    '''
    result = os.popen('lsof -i:%d' % port)

    for index in result.readlines():

        if index.startswith('Python'):
            pid = index.split()[1]
            os.system('kill %s' % pid)

@app.route('/monkeyIndex',methods=['GET','POST'])
def index():
    '''
    首页
    '''
    return render_template('index.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    '''
    传文件
    '''
    f = request.files['file']
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        return render_template('succes.html')
    else:
        return render_template('error.html')

@app.route('/monkeyRun',methods=['GET','POST'])
def runMonkey():
    '''
    运行monkey
    '''
    apkpackagename = str(request.form.get('apkpackagename'))
    runtime = str(request.form.get('runtime'))
    env = str(request.form.get('env'))
    seed = str(request.form.get('seed'))
    #monkey出现bug很难复现，如果传入相同的seed，他们运行的序列一样，可以用来复现bug
    throttle = str(request.form.get('throttle'))
    if throttle == '':
        throttle = 0
    #可以使用这个设置来减缓Monkey的运行速度，不设置的话，则事件之间将没有延迟
    whitelist = str(request.form.get('whitelist'))
    blacklist = str(request.form.get('blacklist'))
    eventcount = str(request.form.get('eventcount'))
    loglevel = str(request.form.get('loglevel'))
    result = EasyRun.run(apkpackagename,runtime,seed,throttle,whitelist,blacklist,env,eventcount,loglevel)
    if result == 0:
        return render_template('runsucces.html')
    else:
        return render_template('runerror.html')

if __name__ == '__main__':
    runflask()
