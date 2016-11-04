# -*-coding:utf-8 -*-
'''
@author :黄鑫晨
@type：返回微信端上传凭证
@datatime：2016.11.4
'''
import json

from BaseHandlerh import BaseHandler
from FileHandler.Upload import AuthKeyHandler


class WgetToken(BaseHandler):

    retjson = {'code': '', "contents": ''}
    def get(self):
        utel = self.get_argument('vali')
        authhandler = AuthKeyHandler()
        self.retjson['contents']= authhandler.get_token_web_one()
