# coding=utf-8
import json
import random

from BaseHandlerh import BaseHandler
from Database.tables import WAcAuth

'''
@author:黄鑫晨
@introduction:返回活动创建权限
每次管理员手动申请后获得认证码
服务器返回验证码，交给活动发布方
活动发布后
'''

class AcAuthFunc(object):
    '''
        生成随机的字符串
    '''

    def get_auth(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(32):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        print salt
        return salt


class AcAuthHandler(BaseHandler):
    def get(self):
        auth_handler = AcAuthFunc()
        auth_string = auth_handler.get_auth()
        retjson = {'auth': auth_string}
        new_ac_auth = WAcAuth(
          WAauth = auth_string
        )
        self.db.merge(new_ac_auth)
        try:
            self.db.commit()
        except Exception, e:
            print e
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)