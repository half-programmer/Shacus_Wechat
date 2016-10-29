# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户
@datatime：2016.10.26
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, WApInfo, WAppointment,WAppointEntry
from Userinfo.Usermodel import decode_base64
from messsage import selectmessage


class WAPselect(BaseHandler):

    retjson = {'code': '', "contents": ''}
    def get(self):

        phone = self.get_argument('phone')
        r_id = self.get_argument('registid')
        ap_id = self.get_argument("apid")
        type = self.get_argument('type')

        user = self.db.query(User).filter(User.Utel == phone).one()
        uid = user.Uid
        regiset = self.db.query(User).filter(User.Uid == r_id).one()
        u_phone = decode_base64(phone)
        r_phone = decode_base64(regiset.Utel)
        appointment =self.db.query(WAppointment).filter(WAppointment.WAPid == ap_id).one()
        aptitle = appointment.WAPtitle
        try:
            exist = self.db.query(WApInfo).filter(WApInfo.WAIappoid == ap_id).one()
            self.retjson['code'] = '10291'
            self.retjson['contents'] = '此约拍已经选择'
        except Exception,e:
            print e
            new_item = ''
            if int(type) == 0:
                new_item = WApInfo(
                    WAImid=r_id,
                    WAIpid=uid,
                    WAIappoid=ap_id,
                )
            else:
                new_item = WApInfo(
                    WAImid=uid,
                    WAIpid=r_id,
                    WAIappoid=ap_id,
                )
            self.db.merge(new_item)
            try:
                self.db.commit()
                self.retjson['code'] = '10293'
                self.retjson['contents'] = r_phone
                ap = self.db.query(WAppointment).filter(WAppointment.WAPid == ap_id).one()
                ap.WAPstatus +=1
                apentry = self.db.query(WAppointEntry).filter(WAppointEntry.WAEapid==ap_id,WAppointEntry.WAEregisterID == r_id).one()
                apentry.WAEchoosed =1
                self.db.commit()
                selectmessage(r_phone,aptitle,u_phone)
            except Exception,e:
                print e
                self.retjson['code'] = '10292'
                self.retjson['contents'] = '服务器错误'

            callback = self.get_argument("jsoncallback")
            jsonp = "{jsfunc}({json});".format(jsfunc=callback,json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
            self.write(jsonp)
