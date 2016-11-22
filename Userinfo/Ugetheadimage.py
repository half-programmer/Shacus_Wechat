# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户获得电话
@datatime：2016.10.29
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, UserImage
from FileHandler.Upload import AuthKeyHandler

class Ugetheadimage(BaseHandler):

    retjson = {'code': '', 'contents': '',}

    def get(self):
        u_id = self.get_argument("uid")
        try:
            auth = AuthKeyHandler()
            headimg = self.db.query(UserImage).filter(UserImage.UIuid == u_id,UserImage.UIvalid == 1).one()
            headimg_url = auth.download_abb_url(headimg.UIurl)
            self.retjson['code'] = '11100'
            self.retjson['contents'] = headimg_url
        except Exception,e:
            print e
            self.retjson['code'] = '11101'
            self.retjson['contents'] = '验证不成功'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)