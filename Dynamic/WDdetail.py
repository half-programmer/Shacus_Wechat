# -*- coding:utf-8 -*-
'''
   @兰威
   @datatime：2016.11.22
   @type：动态详情
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, WDynamic, WDImage
from WDmodel import WDmodel

class WDdetail(BaseHandler):

    retjson = {'code': '', 'contents': ''}

    def get(self):

        phone = self.get_argument("vali")
        d_id = self.get_argument("did")
        wdmodel = WDmodel()
        try:
            exist = self.db.query(User).filter(User.Utel == phone, User.Uvalid == 1).one()
            try:
                dynamic = self.db.query(WDynamic).filter(WDynamic.WDid == d_id,WDynamic.WDvalid == 1).one()
                picurls = self.db.query(WDImage).filter(WDImage.WDIwdid == d_id,WDImage.WDIvalid == 1).all()
                retdata = wdmodel.wd_model_multiply_one(dynamic,picurls)
                self.retjson['code'] = '20022'
                self.retjson['contents'] = retdata
            except Exception,e:
                print e
                self.retjson['code'] = '20021'
                self.retjson['contents'] = '动态不合法'
        except Exception, e:
            print e
            self.retjson['code'] = '20020'
            self.retjson['contents'] = '用户不合法'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)