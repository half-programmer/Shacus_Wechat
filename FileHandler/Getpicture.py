# -*-coding:utf-8 -*-
'''
@author :兰威
@type：返回微信端图片下载地址
@datatime：2016.11.5
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User
from FileHandler.Upload import AuthKeyHandler


class Getpicture(BaseHandler):

    retjson = {'code': '', 'contents': ''}
    def get(self):
        phone = self.get_argument("vali")
        picname = self.get_argument("key")
        try:
            exist = self.db.query(User).filter(User.Utel == phone).one()
            auth = AuthKeyHandler()
            picurl = auth.download_url(picname)
            self.retjson['code'] = '10901'
            self.retjson['contents'] = picurl
        except Exception,e:
            self.retjson['code'] = '10900'
            self.retjson['contents'] = '用户不存在'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)