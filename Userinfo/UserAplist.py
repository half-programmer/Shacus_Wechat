#-*- coding:utf-8 -*-

'''
@王佳镭
@2016.10.26
'''
import json

from sqlalchemy import desc


from BaseHandlerh import  BaseHandler
from Database.tables import  User,  WAppointEntry, WApImage, WAppointment
from Appointment.WAPmodel import WAPmodel
from FileHandler.Upload import AuthKeyHandler


class UserAplist(BaseHandler): #关于用户的一系列约拍

    retjson = {'code': '400', 'contents': 'none'}
    def get(self):
        uid = self.get_argument('id')
        aps = []
        try:
            userinfo = self.db.query(User).filter(User.Uid == uid).one()
            try:
                try:
                    as_register_entries = self.db.query(WAppointEntry).filter(WAppointEntry.WAEregisterID == uid,WAppointEntry.WAEvalid == 1).all()
                    for as_register_entry in as_register_entries:
                        try:
                            ap = self.db.query(WAppointment).filter(as_register_entry.WAEapid == WAppointment.WAPid , WAppointment.WAPvalid == 1).one()
                            aps.append(ap)
                        except Exception, e:
                            print e
                except Exception, e:
                    print "未参加过约拍"
                try:
                    as_sponsors_entries = self.db.query(WAppointment).filter(WAppointment.WAPsponsorid == uid , WAppointment.WAPvalid == 1).all()
                    for appointment in as_sponsors_entries:
                        aps.append(appointment)
                except Exception, e:
                    print "未发起过约拍"
                retdata = []
                auth = AuthKeyHandler()
                wapmodel = WAPmodel()
                for item in aps:
                    aplurl = self.db.query(WApImage).filter(WApImage.WAPIapid == item.WAPid).all()
                    #APurl = auth.download_url(aplurl[0].WAPIurl)
                    if aplurl:
                        retdata01 = wapmodel.wap_model_simply_one(item ,aplurl[0].WAPIurl)
                        retdata.append(retdata01)
                self.retjson['code'] = '200'
                self.retjson['contents'] = retdata
            except Exception, e:
                print e
                self.retjson['code'] = '10603'
                self.retjson['contents'] = '你还没有参加过任何约拍'
        except Exception, e:
            print e
            self.retjson['code']='10604'
            self.retjson['contents']='没有此用户'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
