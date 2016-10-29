# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户获得电话
@datatime：2016.10.29
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import WApInfo, User
from Userinfo.Usermodel import decode_base64


class WAPtel(BaseHandler):

    retjson = {'code': '', "contents": ''}
    def get(self):

        w_phone = self.get_argument('phone')  #当前用户的电话
        w_rid = self.get_argument('rid')     #选择人的id
        w_type = self.get_argument('type')   #约拍类型
        w_apid = self.get_argument('apid')

        user = self.db.query(User).filter(User.Utel == w_phone).one()
        w_uid = user.Uid
        if w_type == 0:
            exist = self.db.query(WApInfo.WAIappoid == w_apid,WApInfo.WAIpid == w_uid,WApInfo.WAImid == w_rid).all()
            if exist:
                user = self.db.query(User).filter(User.Uid == w_rid).one()
                phone = decode_base64(user.Utel)
                self.retjson['code'] = '10410'
                self.retjson['contents'] = phone
            else:
                self.retjson['code'] = '10411'
                self.retjson['contents'] = '无法获得'
        if w_type == 1:
            exist = self.db.query(WApInfo.WAIappoid == w_apid, WApInfo.WAIpid == w_rid, WApInfo.WAImid == w_uid ).all()
            if exist:
                user = self.db.query(User).filter(User.Uid == w_rid).one()
                phone = decode_base64(user.Utel)
                self.retjson['code'] = '10410'
                self.retjson['contents'] = phone
            else:
                self.retjson['code'] = '10411'
                self.retjson['contents'] = '无法获得'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)





