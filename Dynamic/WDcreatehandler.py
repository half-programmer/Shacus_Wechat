# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的发布动态
@datatime：2016.11.22
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, WDynamic
from FileHandler.ImageHandler import ImageHandler


class WDcreatehandler(BaseHandler):

    retjson = {'code': '', 'contents': ''}
    def get(self):
        phone = self.get_argument("vali")
        contents = self.get_argument("contents")
        pics = self.get_arguments('keys[]', strip=True)
        try:
            user = self.db.query(User).filter(User.Utel == phone,User.Uvalid == 1).one()
            u_id = user.Uid
            new_dynamic = WDynamic(
                WDsponsorid=u_id,
                WDcontents=contents,
                WDvalid=0,
            )
            self.db.merge(new_dynamic)
            try:
                self.db.commit()
                wdynamic = self.db.query(WDynamic).filter(WDynamic.WDsponsorid == u_id,WDynamic.WDcontents == contents,WDynamic.WDvalid == 0).one()
                wdy_id = wdynamic.WDid
                image = ImageHandler()
                image.insert_wdynamic_image(pics,wdy_id)
                wdynamic.WDvalid = 1
                self.db.commit()
                self.retjson["code"] = '20002'
                self.retjson["contents"] = '发布动态成功'
            except Exception,e:
                print e
                self.db.roolback()
                self.retjson["code"] = '20001'
                self.retjson["contents"] = '服务器错误'
        except Exception,e:
            print e
            self.retjson["code"] = '20000'
            self.retjson["contents"] = '用户不合法'
        # callback = self.get_argument("jsoncallback")
        # jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        # self.write(jsonp)
            self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

