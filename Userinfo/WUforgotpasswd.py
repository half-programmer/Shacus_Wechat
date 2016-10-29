# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户
@datatime：2016.10.26
'''
import base64
import json

from BaseHandlerh import BaseHandler
from Database.tables import Verification, User
from RegistandLogin.WRegisterHandler import generate_verification_code
from RegistandLogin.WloginHandler import md5
from messsage import message


class WUforgotpasswd(BaseHandler):

    retjson = {'code': '', "contents": ''}

    def get(self):
        m_phone = self.get_argument('phone')
        type = self.get_argument('type')
        if type == '11000':
            utel = base64.encodestring(m_phone)
            utel = utel.replace('\n', '')
            try:
                user = self.db.query(User).filter(User.Utel == utel).one()
                if user:
                    code = generate_verification_code()
                    veri = Verification(
                        Vphone=m_phone,
                        Vcode=code,
                    )
                    self.db.merge(veri)
                    try:
                        self.db.commit()
                        self.retjson['code'] = '11002'  # success
                        self.retjson['contents'] = u'手机号验证成功，发送验证码'
                    except:
                        self.db.rollback()
                        self.retjson['code'] = '11003'  # Request Timeout
                        self.retjson['contents'] = u'服务器错误'
                    message(code, m_phone)
            except Exception,e:
                self.retjson['code'] = '11004'  # success
                self.retjson['contents'] = '该手机未注册'
        if type == '11001':
            m_phone = self.get_argument('phone')
            code = self.get_argument('code')
            try:
                item = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # exist = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # delta = datetime.datetime.now() - exist.VT
                if item.Vcode == code:
                    # if delta<datetime.timedelta(minutes=10):
                    self.retjson['code'] = '11008'
                    self.retjson['contents'] = u'验证成功'
                else:
                    self.retjson['code'] = '10006'
                    self.retjson['contents'] = u'验证码验证失败'
            except:
                self.retjson['code'] = '10007'
                self.retjson['contents'] = u'该手机号码未发送验证码'
        if type == '11002':
            m_phone = self.get_argument('phone')
            code = self.get_argument('code')
            m_password = self.get_argument('password')
            try:
                item = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # exist = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                # delta = datetime.datetime.now() - exist.VT
                if item.Vcode == code:
                    # if delta<datetime.timedelta(minutes=10):
                    self.retjson['code'] = '11005'
                    self.retjson['contents'] = u'修改密码成功'
                    m_password = md5(m_password)
                    m_phone = base64.encodestring(m_phone)
                    m_phone = m_phone.replace("\n", "")
                    user = self.db.query(User).filter(User.Utel == m_phone).one()
                    user.Upassword =m_password
                    self.db.commit()
                    # else :
                    # self.retjson['code'] = 10006
                    # self.retjson['contents'] = u'验证码验证失败'
                else:
                    self.retjson['code'] = '10006'
                    self.retjson['contents'] = u'验证码验证失败'
            except:
                self.retjson['code'] = '10007'
                self.retjson['contents'] = u'该手机号码未发送验证码'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
