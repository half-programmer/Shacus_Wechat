# -*- coding: utf-8 -*-

'''
@type:微信获取JSSDK签名
@author:兰威
@datatime : 2016.10.1
'''
import json

from tornado.escape import json_encode

from BaseHandlerh import BaseHandler

from WJS import WJS
from Wconf import Wconf
class WgetSign(BaseHandler):

    def get(self):
        ret = []
        conf = Wconf.conf

        type = self.get_argument('type')
        appsecret = self.get_argument("appsecret")
        if appsecret == conf.appsecret:
            #ip = self.request.remote_ip
            #url = 'http://%s:80/WgetSign.html'%ip
            #url = 'http://e1b3b8b0.ngrok.io/WgetSign.html'
            #url = 'http://shacuswechat.tunnel.2bdata.com/{}'.format(type)
            url = '{}'.format(type)
            wjs = WJS(url)
            ret = wjs.sign()
            callback = self.get_argument("jsoncallback")
            jsonp = "{jsfunc}({json});".format(jsfunc=callback,json=json_encode(ret))
            self.write(jsonp)





