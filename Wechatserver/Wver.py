# -*- coding: utf-8 -*-
'''
端口验证
'''
import json

import tornado.web
from Wconf import Wconf
from wechat_sdk import WechatBasic

class Wver(tornado.web.RequestHandler):


    conf = Wconf.conf
    def get(self):
        w_signature = self.get_argument('signature')
        w_timestamp = self.get_argument('timestamp')
        w_nonce = self.get_argument('nonce')
        w_echostr = self.get_argument('echostr')

        wechat = WechatBasic(conf=self.conf)
        if wechat.check_signature(w_signature,w_timestamp,w_nonce):
            print "成功了"
            self.write(json.dumps(int(w_echostr)))
        else:
            print "失败了"

