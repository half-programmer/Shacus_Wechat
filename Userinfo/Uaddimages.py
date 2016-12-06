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
        u_id = self.get_argument('id')
        images = self.get_arguments('images[]',strip=True)

        image = UserImgHandler()
        try:
            userinfo = self.db.query(User).filter(User.Uid == u_id).one()  # 获取用户手机
            image.delete_Homepage_image(userinfo.Utel)
            image.change_Homepage_image(images , userinfo.Utel)
            self.db.commit()

            #服务器测试代码(查看数据库是否修改)：
            # imageinfo = self.db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid ,Homepageimage.HPimgvalid==1).all()
            # retdata = []
            # for item in imageinfo:
            #    retdata.append(item.HPimgurl)


            self.retjson['code']='10610'
            self.retjson['contents'] = '修改成功'
        except Exception,e:
            print e
            self.retjson['code'] = '10611'
            self.retjson['contents'] = '没有找到该用户'
        #callback = self.get_argument("jsoncallback")
        #jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        #self.write(jsonp)
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))


