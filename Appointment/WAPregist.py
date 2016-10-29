# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍报名
@datatime：2016.10.25
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import WAppointment, WAppointEntry, User


class WAPregist(BaseHandler):

    retjson = {'code':'','contents':''}
    def db_error(self):
        self.db.rollback()
        self.retjson['contents'] = '数据库插入错误'
        self.retjson['code'] = '10274'

    def get(self):
        phone = self.get_argument('phone')
        ap_id = self.get_argument('apid')
        user = self.db.query(User).filter(User.Utel == phone).one()
        u_id = user.Uid
        appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == ap_id, WAppointment.WAPstatus == 1,WAppointment.WAPvalid==1).one()
        try:
                exist = self.db.query(WAppointEntry). \
                    filter(WAppointEntry.WAEregisterID == u_id, WAppointEntry.WAEapid == ap_id
                    ).one()  # 应该再加上和ap_id的验证
                if exist.WAEvalid == 1:
                            self.retjson['contents'] = '已报名过该约拍'
                            self.retjson['code'] = '10273'
                else:
                    exist.WAEvalid = 1
                    appointment.WAPregistN += 1
                    self.db.commit()
                    self.retjson['contents'] = '报名成功'
                    self.retjson['code'] = '10270'
        except Exception, e:
                print e
                print "插入之前"
                new_appointmententry = WAppointEntry(
                    WAEapid=ap_id,
                    WAEregisterID=u_id,
                    WAEvalid=1,
                    WAEchoosed=0,
                )
                try:
                    appointment.WAPregistN += 1
                except Exception,e:
                    self.retjson['contents'] = '报名人数增加错误'
                self.db.merge(new_appointmententry)
                try:
                    self.db.commit()
                    self.retjson['contents'] = '用户报名成功'
                    self.retjson['code'] = '10270'
                except Exception, e:
                    print e
                    self.db_error()
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)