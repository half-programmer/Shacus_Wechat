# -*-coding:utf-8 -*-
'''
@author :兰威
@type：获取要修改的信息
@datatime：2016.10.10
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import WAppointment, User
from Appointment.WAPmodel import WAPmodel

class WAPgetchangeinfo(BaseHandler):

    retjson = {'code': '', 'contents': ''}
    def get(self):
        phone = self.get_argument("vali")
        id =self.get_argument("id")

        try:
            uid = self.db.query(User).filter(User.Utel == phone).one()
            try:
                wap = self.db.query(WAppointment).filter(WAppointment.WAPid == id,WAppointment.WAPsponsorid == uid ).one()
                ret_ap = WAPmodel.wap_model_getchangeinfo(wap)
                self.retjson['code'] = '11102'
                self.retjson['contents'] = ret_ap
            except Exception,e:
                print e
                self.retjson['code'] = '11101'
                self.retjson['contents'] = '你不是该约拍的发布者'
        except Exception,e:
            print e
            self.retjson['code'] = '11100'
            self.retjson['contents'] = '该用户不存在'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)