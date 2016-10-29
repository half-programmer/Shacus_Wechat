# -* coding:utf-8 *-
'''
@author:黄鑫晨
@time:2016-10-27
@intro：修改（完善）邮箱，修改密码
'''
import json

import re

from BaseHandlerh import BaseHandler
from Database.tables import User
from RegistandLogin.WloginHandler import md5

class UinfoHandler(BaseHandler):
    retjson = {'code':'', 'contents':''}

    def commit(self):
        try:
            self.db.commit()
        except Exception, e:
            self.retjson['code'] = u'500'
            self.retjson['contents'] = u"数据库提交错误"

    def validateEmail(self,email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return 1
        return 0

    def get(self):
        utel = self.get_argument('utel')
        type = self.get_argument('type')
        callback = self.get_argument("jsoncallback")
        try:
            user = self.db.query(User).filter(User.Utel == utel).one()
            old_password = user.Upassword  # 旧密码

            if user:
                if type == '1':  # 修改邮箱
                    mailbox = self.get_argument('mailbox')
                    if self.validateEmail(mailbox):  # 邮箱格式正确
                        user.Umailbox = mailbox
                        self.retjson['code'] = '20001'
                        self.retjson['contents'] = u'修改邮箱成功'
                    else:
                        self.retjson['code'] = '40001'
                        self.retjson['contents'] = u'邮箱格式错误'

                if type == '2':  # 修改密码
                    o_password = self.get_argument('old_password')
                    if old_password == md5(o_password):
                        new_password = self.get_argument('new_password')
                        user.Upassword = md5(new_password)
                        self.retjson['code'] = '20002'
                        self.retjson['contents'] = u'修改密码成功'
                        self.commit()
                    else:  # 旧密码错误
                        self.retjson['code'] = u'40002'
                        self.retjson['contents'] = u'旧密码错误'
        except Exception, e:
            print e
            self.retjson['code'] = '40000'
            self.retjson['contents'] = u'该用户不存在'

        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
