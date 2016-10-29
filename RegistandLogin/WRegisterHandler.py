# -*- coding:utf-8 -*-
'''
@author 兰威
type :用户注册
'''
import base64
import hashlib
import json
import random

import datetime
from sqlalchemy import desc
from tornado.escape import json_encode

from  BaseHandlerh import BaseHandler
from Database.tables import User,  Image, UserImage, NewChoosed
from Database.tables import Verification
from Userinfo import Usermodel
from Userinfo.Usermodel import user_login_fail_model
from messsage import message
import os, time



def session_id():
    return hashlib.sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()


def generate_verification_code(len=6):
    ''' 随机生成6位的验证码 '''
    # 注意： 这里我们生成的是0-9的列表，当然你也可以指定这个list，这里很灵活
    code_list = []
    for i in range(10): # 0-9数字
        code_list.append(str(i))
    myslice = random.sample(code_list, len) # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice) # list to string
    return verification_code
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


class WRegisterHandler(BaseHandler):
    print "进入regist"
    retjson = {'code': '400', 'contents': 'None'}
    def get(self):
        callback = self.get_argument("jsoncallback")
        type = self.get_argument('type', default='unsolved')
        if type == '10001':  # 验证手机号
            m_phone=self.get_argument('phone')
            try:
                utel = base64.encodestring(m_phone)
                utel = utel.replace('\n','')
                user = self.db.query(User).filter(User.Utel == utel).one()
                if user:
                    self.retjson['contents'] = u"该手机号已经被注册，请更换手机号或直接登录"
                    self.retjson['code'] = 10005
            except:
                code=generate_verification_code()
                veri=Verification(
                    Vphone=m_phone,
                    Vcode=code,
                )
                self.db.merge(veri)
                try:
                    self.db.commit()
                    self.retjson['code'] = 10004 # success
                    self.retjson['contents'] = u'手机号验证成功，发送验证码'
                except:
                    self.db.rollback()
                    self.retjson['code'] = 10009  # Request Timeout
                    self.retjson['contents'] = u'服务器错误'
                message(code, m_phone)
        elif type=='10002': #验证验证码
            m_phone=self.get_argument('phone')
            code=self.get_argument('code')
            try:
               item=self.db.query(Verification).filter(Verification.Vphone==m_phone).one()
               #exist = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
               #delta = datetime.datetime.now() - exist.VT
               if item.Vcode==code:
                   #if delta<datetime.timedelta(minutes=10):
                    self.retjson['code']=10004
                    self.retjson['contents']=u'验证码验证成功'
                   #else :
                       #self.retjson['code'] = 10006
                       #self.retjson['contents'] = u'验证码验证失败'
               else:
                   self.retjson['code']=10006
                   self.retjson['contents']=u'验证码验证失败'
            except:
                self.retjson['code']=10007
                self.retjson['contents']=u'该手机号码未发送验证码'

        elif type=='10003': #注册详细信息
            m_password=self.get_argument('password')
            m_nick_name=self.get_argument('nickName')  # 昵称
            m_phone=self.get_argument('phone')
            m_sex = self.get_argument('sex')    #性别
            try:
                m_phone = base64.encodestring(m_phone)
                m_phone = m_phone.replace("\n","")
                m_password = md5(m_password)
                same_nickname_user = self.db.query(User).filter(User.Uname == m_nick_name).one()#临时判断
                if same_nickname_user:  # 该昵称已被使用
                    self.retjson['code'] = '10008'  # Request Timeout
                    self.retjson['contents'] ="该昵称已被使用"
            except: # 手机号和昵称皆没有被注册过
                    new_user = User(
                        Upassword=m_password,
                        Ualais=m_nick_name,
                        Utel=m_phone,
                        Usex=m_sex,
                    )
                    self.db.merge(new_user)
                    try:
                        self.db.commit()
                        image = Image(
                            IMvalid=True,
                            IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                            IMname=m_nick_name
                        )

                        self.db.merge(image)
                        self.db.commit()
                        m_id = self.db.query(User.Uid).filter(User.Utel == m_phone).one()
                        new_img = self.db.query(Image).filter(Image.IMname == m_nick_name).one()
                        imid = new_img.IMid
                        userImage = UserImage(
                            UIuid = m_id[0],
                            UIimid = imid,
                            UIurl = "user-default-image.jpg"
                        )
                        self.db.merge(userImage)
                        self.db.commit()
                        # self.retjson['contents'] = retdata
                        new_choosed_entry = NewChoosed(
                            uid=user.Uid,
                            choosed=0
                        )
                        self.db.merge(new_choosed_entry)
                        try:
                            self.db.commit()
                        except Exception, e:
                            self.retjson['code'] = '500'
                            self.retjson['contents'] = u'数据库提交失败'

                        self.retjson['contents'] = m_phone
                        self.retjson['code'] = 10004  # success

                    except Exception, e:
                        print e
                        self.db.rollback()
                        self.retjson['code'] = 10009  # Request Timeout
                        self.retjson['contents'] = u'Some errors when commit to database, please try again'
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)

