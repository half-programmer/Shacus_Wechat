#-*- coding:utf-8 -*-
from BaseHandlerh import BaseHandler
from Database.tables import Homepageimage, User


class Ugetimage(BaseHandler):
    retjson={'code':'200','contents':'null'}
    def __get__(self):
        u_phone = self.get_argument('phone')
        userinfo = self.db.query(User).filter(User.Utel == u_phone).one()  # 获取用户id
        imageinfo = self.db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid,
                                                        Homepageimage.HPimgvalid == 1).all()
        retdata = []
        for item in imageinfo:
            retdata.append(item.HPimgurl)
        self.retjson['code'] = '10612'
        self.retjson['contents'] = retdata