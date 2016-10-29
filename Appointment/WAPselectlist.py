# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍选择报名用户
@datatime：2016.10.26
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import WAppointEntry, WAppointment, User, WApInfo
from Appointment.WAPusermodel import wechat_user_model_simply


class WAPselectlist(BaseHandler):

    retjson = {'code':'',"contents":''}

    def get(self):

        m_ap_id = self.get_argument('apid')
        phone = self.get_argument('phone')
        user = self.db.query(User).filter(User.Utel == phone).one()
        m_u_id = user.Uid

        try:
            #exist = self.db.query(WAppointment).filter(WAppointment.WAPsponsorid == m_u_id,WAppointment.WAPid == m_ap_id).one()
            apentrys = self.db.query(WAppointEntry).filter(WAppointEntry.WAEapid == m_ap_id,WAppointEntry.WAEvalid == 1).all()
            retdata = []
            for apentry in apentrys:
                userid = apentry.WAEregisterID
                user = self.db.query(User).filter(User.Uid == userid).one()
                if apentry.WAEchoosed == 1:
                    self.retjson["choosedid"] = userid
                retdata_item = wechat_user_model_simply(user)
                retdata.append(retdata_item)
            self.retjson['code'] = '10281'
            self.retjson['contents'] = retdata


        except Exception,e:
            print e
            self.retjson['code'] ='10280'
            self.retjson['contents'] = '不是该用户发布的活动'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
