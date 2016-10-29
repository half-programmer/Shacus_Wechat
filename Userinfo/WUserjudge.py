# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户获得电话
@datatime：2016.10.29
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User


class WUserjudge(BaseHandler):


    retjson = {'code': '', 'contents': ''}
    def get(self):

        u_id = self.get_argument('id')
        phone = self.get_argument("phone")

        try:
            exist = self.db.query(User).filter(User.Uid == u_id,User.Utel == phone).one()
            self.retjson['code'] = '10500'
            self.retjson['contents'] = '验证成功'
        except Exception,e:
            self.retjson['code'] = '10501'
            self.retjson['contents'] = '验证不成功'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)