# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍取消报名
@datatime：2016.10.25
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import WAppointment, WAppointEntry, User


class WAPregistcancel(BaseHandler):

    def db_error(self):
        self.db.rollback()
        self.retjson['contents'] = '数据库插入错误'
        self.retjson['code'] = '10274'

    retjson = {'code':'',"contents":""}

    def get(self):

        ap_id = self.get_argument("apid")
        phone = self.get_argument("phone")
        user = self.db.query(User).filter(User.Utel == phone).one()
        ap_user_id = user.Uid
        try:
            exist = self.db.query(WAppointEntry).filter(
                WAppointEntry.WAEregisterID == ap_user_id, WAppointEntry.WAEapid == ap_id).one()
            appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == ap_id).one()
            if appointment.WAPstatus == 1:  # 报名中：
                # todo 应该再加上和ap_id的验证
                if exist.WAEvalid:
                    exist.WAEvalid = 0
                    try:
                        appointment.WAPregistN -= 1
                        self.db.commit()
                        self.retjson['contents'] = '取消报名成功'
                        self.retjson['code'] = '10276'
                    except Exception, e:
                        print e
                        self.db.rollback()
                        self.db_error()
                else:
                    self.retjson['contents'] = '用户已经取消报名'
                    self.retjson['code'] = '10277'
            else:
                self.retjson['contents'] = '该约拍不在报名中，不能取消报名'
                self.retjson['code'] = '10260'

        except Exception, e:
            print e
            self.retjson['contents'] = '用户未报名过该约拍'
            self.retjson['code'] = '10278'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)