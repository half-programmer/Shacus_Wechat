# coding=utf-8
'''
@author: 黄鑫晨
'''
import base64
import hashlib
import json

import tornado
from sqlalchemy import desc
from tornado import gen
from tornado.concurrent import Future
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import  User, NewChoosed
from Userinfo import Usermodel
#from Userinfo.Ufuncs import Ufuncs
from Userinfo.Usermodel import Model_daohanglan

def md5(str):  # 加密
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


class WLoginHandler(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}


    @asynchronous
    @gen.coroutine
    def get(self):

        m_phone = self.get_argument('phone')
        m_password = self.get_argument('password')
        m_phone = base64.encodestring(m_phone)
        m_phone = m_phone.replace("\n","")
        m_password = md5(m_password)
        if not m_phone or not m_password:
            self.retjson['code'] = 400
            self.retjson['contents'] = 10105  # '用户名密码不能为空'
        #todo:登录返回json的retdata多一层[]，客户端多0.5秒处理时间
        # 防止重复注册
        else:
            try:
                user = self.db.query(User).filter(User.Utel == m_phone).one()

                if user:  # 用户存在
                    password = user.Upassword
                    if m_password == password:  # 密码正确
                        self.retjson['contents'] = dict(
                            phone=m_phone,
                            id=user.Uid
                        )
                        self.retjson['code'] = 10004  # success
                    else:
                        self.retjson['contents'] = u'密码错误'
                        self.retjson['code'] = '10114'  # 密码错误
                else:  # 用户不存在
                    self.retjson['contents'] = u'该用户不存在'
                    self.retjson['code'] = '10113'
            except Exception, e:  # 还没有注册
                print "异常："
                print e
                self.retjson['contents'] = u'该用户名不存在'
                self.retjson['code'] = '10113'  # '该用户名不存在'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)