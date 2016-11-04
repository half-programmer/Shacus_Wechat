# -*-coding:utf-8 -*-
'''
@author :黄鑫晨
@type：返回微信端上传凭证
@datatime：2016.11.4
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User
from FileHandler.Upload import AuthKeyHandler


class WgetToken(BaseHandler):

    retjson = {"uptoken":"xxx:xxx:xxx"}
    def get(self):
        utel = self.get_argument('vali')
        try:
            user = self.db.query(User).filter(User.Utel == utel).one()
            authhandler = AuthKeyHandler()
            self.retjson['uptoken'] = authhandler.get_token_web_one()
        except Exception:
            self.retjson['uptoken'] = u'用户认证出错'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文
