# -*- coding: utf-8 -*-
'''
微信JS-SDK操作
'''
import random
import string

import time
from wechat_sdk import WechatBasic
from Wconf import Wconf
from BaseHandlerh import BaseHandler

class WJS(BaseHandler):

    conf = Wconf.conf
    wechat = WechatBasic(conf=conf)

    def __init__(self,url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        self.ret['signature'] = self.wechat.generate_jsapi_signature(self.ret['timestamp'],self.ret['nonceStr'],self.ret['url'])
        return self.ret