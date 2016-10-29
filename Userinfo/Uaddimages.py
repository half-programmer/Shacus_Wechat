# -*— coding:utf-8 -*-
'''
author:wjl
2016.10.27
'''
from BaseHandlerh import BaseHandler
from Database.tables import User, WAppointment
from FileHandler.ImageHandler import ImageHandler
from Userinfo.UserImgHandler import UserImgHandler
from Wechatserver.Wpichandler import Wpichandler
import json
class Uaddimages(BaseHandler):#用户在个人主页增加图片
    retjson={'code':'200','contents':'none'}
    def get(self):
        u_phone = self.get_argument('phone')
        images = self.get_arguments('image[]',strip=True)
        wpicture = Wpichandler()
        image = UserImgHandler()
        if wpicture.pichandler(images,images):
            image.insert_Homepage_image(images,u_phone)
        self.retjson['contents'] = '上传主页图片成功'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


