# -*- coding:utf-8 -*-
'''
@author 兰威
@type 发送短信验证码
'''

import sys, urllib, urllib2, json
def message(code=000000,phone=00000000000):
   url = "http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile="+phone+"&content=尊敬的追影用户您好，您的验证码为："+code+"，请不要告诉别人哦！【追影】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if(str):
       print(str)
def selectmessage(phone=00000000000,appointment='lalala',selectphone=00000000000):
   url = "http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile=" + phone + "&content=尊敬的追影用户您好，您在"+appointment+"约拍中被选择为约拍对象，选择您的用户联系方式为"+selectphone+"。请在追影南京公众号-进入系统-个人主页-我的约拍-详情中查看【追影】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if (str):
      print(str)

def remindmessage(phone=00000000000,appointment='lalala'):
   url = "http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile=" + phone + "&content=尊敬的追影用户您好，您的约拍"+appointment+"已经有人报名了，记得经常查看约拍，不要让您的摄友等太久哦！【追影】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if (str):
      print(str)

def passVerifymessage(phone=00000000000,activity='lalala'):
   url="http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile="  +phone  +"&content=尊敬的追影用户你好，您的活动"+activity+"已经通过审核，您可以在追影南京公众号-进入系统后查看啦，祝您活动举办成功!【追影】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if (str):
      print(str)