# coding=utf-8

'''
发送邮件类
@author xinxi
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
from MailConfig import *
from AdbCommon import AdbCommon
from FileCommon import *
import time
import sys
import logger
reload(sys)

sys.setdefaultencoding('utf8')

debug = False
def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.apk':
                L.append(os.path.join(root, file))
    return L

def _joincontenterror(Runtime, mobilebrand, mobilesysversion, cmd, writerror,crashnum,anrnumber,noresponsenum,exceptionnum):
    '''
    拼接邮件中content内容
    :return:
    '''
    base_dir = os.path.dirname(__file__)
    apkdir = os.path.join(base_dir) + '/TestApp'
    try:
        with open(writerror, 'r') as f:
            error = f.read()

        sendtime = time.strftime("%Y-%m-%d %H:%M:%S")
        # 定义发生时间
        content = ''' 

Monkey测试时长: %s秒

Monkey测试设备型号: %s

Monkey测试设备系统版本: %s

Monkey测试APP: %s

Monkey执行命令：%s

Crash错误数：%s       ANR错误数：%s       No Response错误数：%s      Exception错误数：%s

错误日志标记: %s

monkey日志详见附件

    ''' % \
                  (Runtime,
                   mobilebrand,
                   mobilesysversion,
                   ''.join(file_name(apkdir)).split('/')[-1],
                   cmd,
                   crashnum,
                   anrnumber,
                   noresponsenum,
                   exceptionnum,
                   '\n' + error)
        return content
    except Exception as e:
        logger.log_error('拼接邮件中content失败: ' + str(e))
        return ''
def _joincontentinfo(Runtime, mobilebrand, mobilesysversion,  cmd,crashnum,anrnumber,noresponsenum,exceptionnum):
    '''
    拼接邮件中content内容
    :return:
    '''
    base_dir = os.path.dirname(__file__)
    apkdir = os.path.join(base_dir) + '/TestApp'
    try:
        sendtime = time.strftime("%Y-%m-%d %H:%M:%S")
        # 定义发生时间
        content = ''' 

Monkey测试时长: %s秒

Monkey测试设备型号: %s

Monkey测试设备系统版本: %s

Monkey测试APP: %s

Monkey执行命令：%s

Crash错误数：%s       ANR错误数：%s       No Response错误数：%s      Exception错误数：%s

monkey日志详见附件

    ''' % \
                  (Runtime,
                   mobilebrand,
                   mobilesysversion,
                   ''.join(file_name(apkdir)).split('/')[-1],
                   cmd,
                   crashnum,
                   anrnumber,
                   noresponsenum,
                   exceptionnum)
        return content
    except Exception as e:
        logger.log_error('拼接邮件中content失败: ' + str(e))
        return ''

def _format_addr(s):
    '''
    格式化姓名和地址
    :param s:
    :return:
    '''
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def send_mail_error(devices,monkeylog, writerror ,runtime,monkeycmd,crashnum,anrnumber,noresponsenum,exceptionnum):
    """
    邮件发送
    params:
    @sub 邮件主题
    @content 邮件正文内容
    to_list:发给谁
    sub:主题
    格式eg：
    content:内容

    格式eg:
    发生时间:
    测试机型：
    monkey执行命令：
    monkey日志：
    错误日志在多少行

    send_mail(发件人地址,邮件主题,邮件正文内容)
    通过Main_Config配置文件读取
    """

    adc = AdbCommon(devices)

    content = _joincontenterror(runtime, adc.getmobilebrand(), adc.getmobileversion(),
                           stringwrap(monkeycmd), writerror,crashnum,anrnumber,noresponsenum,exceptionnum)
    # 邮件正文

    if content != '':
        global s
        global receivers
        if debug == True:
            receivers = debuglist  # 测试邮箱
        else:
            receivers = receiverslist  # 正式邮箱

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = _format_addr(u'发件人<%s>' % mail_user)
        message['To'] = ";".join(receivers)

        subject = 'AndroidMonkey测试结果反馈'

        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的附件文件
        att1 = MIMEText(open(monkeylog).read())
        att1["Content-Type"] = 'application/octet-stream'
        # filename是附件中的名字
        att1["Content-Disposition"] = 'attachment; filename="%s"' % monkeylog.split('/')[-1]
        message.attach(att1)
        # 构造附件2，传送当前目录下的附件文件
        att2 = MIMEText(open(writerror).read())
        att2["Content-Type"] = 'application/octet-stream'
        # filename是附件中的名字
        att2["Content-Disposition"] = 'attachment; filename="%s"' % writerror.split('/')[-1]
        message.attach(att2)

        try:
            s = smtplib.SMTP(mail_host, mail_port)
            # s.set_debuglevel(1)
            s.starttls()
            # s.connect('smtp.partner.outlook.cn', 25)
            s.login(mail_user,mail_pass)
            s.sendmail(mail_user, receivers, message.as_string())
            s.quit()
            logger.log_info("mail send success")

        except Exception, e:
            print str(e)
            logger.log_error("mail send fail" + '\n' + '异常信息:' + str(e))
            s.quit()
    else:
        logger.log_info('未达到报警状态')
def send_mail_info(devices,monkeylog, runtime, monkeycmd,crashnum,anrnumber,noresponsenum,exceptionnum):
    """
    邮件发送
    params:
    @sub 邮件主题
    @content 邮件正文内容
    to_list:发给谁
    sub:主题
    格式eg：
    content:内容

    格式eg:
    发生时间:
    测试机型：
    monkey执行命令：
    monkey日志：
    错误日志在多少行

    send_mail(发件人地址,邮件主题,邮件正文内容)
    通过Main_Config配置文件读取
    """

    adc = AdbCommon(devices)

    content = _joincontentinfo(runtime, adc.getmobilebrand(), adc.getmobileversion(),
                                stringwrap(monkeycmd),crashnum,anrnumber,noresponsenum,exceptionnum)
    # 邮件正文

    if content != '':
        global s
        global receivers
        if debug == True:
            receivers = debuglist  # 测试邮箱
        else:
            receivers = receiverslist  # 正式邮箱

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = _format_addr(u'发件人<%s>' % mail_user)
        message['To'] = ";".join(receivers)

        subject = 'AndroidMonkey测试结果反馈'

        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的附件文件
        att1 = MIMEText(open(monkeylog).read())
        att1["Content-Type"] = 'application/octet-stream'
        # filename是附件中的名字
        att1["Content-Disposition"] = 'attachment; filename="%s"' % monkeylog.split('/')[-1]
        message.attach(att1)

        try:
            s = smtplib.SMTP(mail_host, mail_port)
            # s.set_debuglevel(1)
            s.starttls()
            # s.connect('smtp.partner.outlook.cn', 25)
            s.login(mail_user, mail_pass)
            s.sendmail(mail_user, receivers, message.as_string())
            s.quit()
            logger.log_info("mail send success")

        except Exception, e:
            print str(e)
            logger.log_error("mail send fail" + '\n' + '异常信息:' + str(e))
            s.quit()
    else:
        logger.log_info('未达到报警状态')


