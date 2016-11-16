#-*- coding:utf-8 -*-
import base64
import json
from Database.tables import  User, WAcEntry, WActivity

'''
@author: 黄鑫晨
'''
from BaseHandlerh import BaseHandler
from Userinfo.Usermodel import wechat_user_model_simply
from Userinfo.Usermodel import decode_base64
class WgetUserList(BaseHandler):

    '''
    获得用户列表
    '''
    retjson = {'code':'','contents':''}
    def get(self):
        try:
            users = self.db.query(User).all()
            retdata = []
            for user in users:
                retdata_item = wechat_user_model_simply(user)
                retdata.append(retdata_item)
            self.retjson['code'] = '10400'
            self.retjson['contents'] = retdata

        except Exception, e:
            print e
            self.retjson['code'] = '10401'
            self.retjson['contents'] = '活动不存在'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


