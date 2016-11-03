# -*— coding:utf-8 -*-
'''
author:wjl
2016.10.27
'''
from BaseHandlerh import BaseHandler
from Database.tables import User, WAppointment, Homepageimage
from FileHandler.ImageHandler import ImageHandler
from Userinfo.UserImgHandler import UserImgHandler
from Wechatserver.Wpichandler import Wpichandler
import json
class Uaddimages(BaseHandler):#用户在个人主页增加图片
    retjson={'code':'200','contents':'none'}

    def get(self):
        u_phone = self.get_argument('phone')
        images = self.get_arguments('images[]',strip=True)
        #wpicture = Wpichandler()
        image = UserImgHandler()
        #if wpicture.pichandler(images,images):
        image.insert_Homepage_image(images,u_phone)
        userinfo = self.db.query(User).filter(User.Utel == u_phone).one()#获取用户id
        imageinfo = self.db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid ,Homepageimage.HPimgvalid==1).all()
        retdata = []
        for item in imageinfo:
           retdata.append(item.HPimgurl)
        self.retjson['code']='10610'
        self.retjson['contents'] = retdata
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


