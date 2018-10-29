# coding=utf-8

'''
@property方法取出值
@monkeyfolder.setter 重新设置属性的值
@author:xinxi
'''
import time,os
current_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))

class DateBean(object):

    def __init__(self):
        self._monkeyfolder = 'MonkeyLog'
        self._monkeylog = self._monkeyfolder + '/MonkeyInfo_%s.log' % time.strftime("%Y%m%d%H%M%S")
        self._monkeyerrorlog =  self._monkeyfolder + '/MonkeyError_%s.log' % time.strftime("%Y%m%d%H%M%S")
        self._logdir = 'Log'
        self._writeerror = self._logdir + "/" + time.strftime("%Y%m%d%H%M%S") + "_writeerror.log"

        self._dependlist = [project_dir+'/DependApp/simiasque-debug.apk']

        self._dependname = ['org.thisisafactory.simiasque']

        self._simiasquename = 'org.thisisafactory.simiasque'
        self._simiasqueactivity = 'org.thisisafactory.simiasque.MyActivity_'


    @property
    def monkeyfolder(self):
        return self._monkeyfolder

    @monkeyfolder.setter
    def monkeyfolder(self, value):
        self._monkeyfolder = value

    @property
    def monkeyerrorlog(self):
        return self._monkeyerrorlog

    @monkeyerrorlog.setter
    def monkeyerrorlog(self, value):
        self._monkeyerrorlog = value

    @property
    def monkeylog(self):
        return self._monkeylog

    @monkeylog.setter
    def monkeylog(self, value):
        self._monkeylog = value

    @property
    def logdir(self):
        return self._logdir

    @logdir.setter
    def logdir(self, value):
        self._logdir= value

    @property
    def writeerror(self):
        return self._writeerror

    @writeerror.setter
    def writeerror(self, value):
        self._writeerror = value


    @property
    def dependlist(self):
        return self._dependlist

    @dependlist.setter
    def dependlist(self, value):
        self._dependlist = value

    @property
    def dependname(self):
        return self._dependname

    @dependlist.setter
    def dependlist(self, value):
        self._dependname = value

    @property
    def simiasquename(self):
        return self._simiasquename

    @simiasquename.setter
    def simiasquename(self, value):
        self._simiasquename = value

    @property
    def simiasqueactivity(self):
        return self._simiasqueactivity

    @simiasqueactivity.setter
    def simiasqueactivity(self, value):
        self._simiasqueactivity = value




