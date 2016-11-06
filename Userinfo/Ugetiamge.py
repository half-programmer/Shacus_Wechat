#-*- coding:utf-8 -*-
from BaseHandlerh import BaseHandler
from Database.tables import Homepageimage, User
from FileHandler.Upload import AuthKeyHandler
import json


class Ugetimage(BaseHandler):
    retjson={'code':'200','contents':'null'}
    def get(self):
        u_id = self.get_argument('id')
        try:
            userinfo = self.db.query(User).filter(User.Uid == u_id).one()  # 获取用户id
            auth=AuthKeyHandler()
            imageinfo = self.db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid,
                                                            Homepageimage.HPimgvalid == 1).all()
            retdata = []
            for item in imageinfo:
                url = auth.download_url(item.HPimgurl)
                retdata.append(url)
            self.retjson['code'] = '10612'
            self.retjson['contents']=retdata
        except Exception,e:
            print e
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)