# -*— coding:utf-8 -*-
'''
author:wjl
2016.10.27
'''
import json
from BaseHandlerh import BaseHandler
from Database.tables import User, WAppointment, Homepageimage
from FileHandler.ImageHandler import ImageHandler
from Userinfo.UserImgHandler import UserImgHandler
from Wechatserver.Wpichandler import Wpichandler

class Udeleteimages(BaseHandler):#用户在个人主页删除照片
    retjson={'code':'200','contents':'null'}
    def get(self):
        u_phone = self.get_argument('phone')
        images = self.get_argument('images[]',strip=True)
        userinfo = self.db.query(User).filter(User.Utel == u_phone).one()#为了获取用户id
        retimages = []
        for i in images:
            user = self.db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid , Homepageimage.HPimgurl==images).all()
            for item in user:
                item.HPimgvalid = False
                self.db.commit()

        self.retjson['contents']='删除图片成功'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)