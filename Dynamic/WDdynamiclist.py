# -*- coding:utf-8 -*-
'''
   @兰威
   @datatime：2016.11.22
   @type：回复动态列表
'''
import json

from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Database.tables import User, WDynamic, WDImage
from WDmodel import WDmodel

class WDdynamiclist(BaseHandler):

    retjson = {'code': '', 'contents': ''}
    def get(self):

        phone = self.get_argument("vali")
        row = self.get_argument('row')
        wdmodel = WDmodel()
        retdata = []
        try:
            exist = self.db.query(User).filter(User.Utel == phone,User.Uvalid == 1).one()
            dynamics = self.db.query(WDynamic).filter(WDynamic.WDvalid == 1).order_by(desc(WDynamic.WDcreateT)).offset(int(row)).limit(10).all()
            for dynamic in dynamics:
                data = self.db.query(WDImage).filter(WDImage.WDIwdid == dynamic.WDid,WDImage.WDIvalid == 1).all()
                retdata.append(wdmodel.wd_model_multiply_one(dynamic,data))
            self.retjson['code'] = '20011'
            self.retjson['contents'] = retdata

        except Exception,e:
            print e
            self.retjson['code'] = '20010'
            self.retjson['contents'] = '用户不合法'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
