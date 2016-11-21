# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍提醒
@datatime：2016.11.20
'''
import urllib

f=urllib.urlopen("http://www.shacus.top/weixin/appointment/remind")
s=f.read()
print s