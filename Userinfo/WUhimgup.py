# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户获得电话
@datatime：2016.11.21
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User
from FileHandler.ImageHandler import ImageHandler

class WUhimgup(BaseHandler):

    retjson = {'code': '', 'contents': ''}
    def get(self):

        image = ImageHandler()
        phone = self.get_argument("vali")
        key = self.get_argument("key")
        headpic = []
        headpic.append(key)
        try:
            user = self.db.query(User).filter(User.Utel == phone).one()
            m_id = user.Uid
            image.change_user_headimage(headpic,m_id)
            self.retjson["code"] = "11100"
            self.retjson["contents"] = "上传头像成功"
        except Exception,e:
            print e
            self.retjson["code"] = "11101"
            self.retjson["contents"] = "上传头像失败"
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)