# coding=utf-8
import json

from  BaseHandlerh import BaseHandler
from Database.tables import User
from Userinfo.Ufuncs import Ufuncs

'''
@author:王佳镭 黄鑫晨
'''

class APregistHandler(BaseHandler):  # 报名约拍
    retjson = {'code': '', 'contents': ''}

    def db_error(self):
        self.db.rollback()
        self.retjson['contents'] = '数据库插入错误'
        self.retjson['code'] = '10274'

    def post(self):
        u_id = self.get_argument('uid')
        ap_type = self.get_argument('type')
        ap_id = self.get_argument('apid')
        u_auth_key = self.get_argument('authkey')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(u_id, u_auth_key):  # 用户认证成功
            if ap_type == '10271':  # 报名约拍
                try:
                    ap_user = self.db.query(User).filter(User.Uauthkey == u_auth_key).one()
                    ap_user_id = ap_user.Uid
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id, Appointment.APstatus == 0).one()
                    try:
                        exist = self.db.query(AppointEntry). \
                            filter(AppointEntry.AEregisterID == u_id, AppointEntry.AEapid == ap_id,
                            ).one()  # 应该再加上和ap_id的验证
                        if exist.AEvalid == 1:
                            self.retjson['contents'] = '已报名过该约拍'
                            self.retjson['code'] = '10273'
                        else:
                            exist.AEvalid = 1
                            appointment.APregistN += 1
                            self.db.commit()
                            self.retjson['contents'] = '报名成功'
                            self.retjson['code'] = '10273'
                    except Exception, e:
                        print e
                        print "插入之前"
                        new_appointmententry = AppointEntry(
                            AEapid=ap_id,
                            AEregisterID=ap_user_id,
                            AEvalid=1,
                            AEchoosed=0,
                        )
                        try:
                            appointment.APregistN += 1
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
                except Exception, e:
                    print e
                    self.retjson['contents'] = '授权码不存在或已过期或改活动不存在'
                    self.retjson['code'] = '10279'
            elif ap_type == '10275':  # 用户取消报名
                try:
                    ap_user = self.db.query(User).filter(User.Uauthkey == u_auth_key).one()
                    ap_user_id = ap_user.Uid
                    try:
                        exist = self.db.query(AppointEntry).filter(
                            AppointEntry.AEregisterID == ap_user_id, AppointEntry.AEapid == ap_id).one()
                        appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                        if appointment.APstatus == 0:  # 报名中：
                            #todo 应该再加上和ap_id的验证
                            if exist.AEvalid:
                                exist.AEvalid = 0
                                try:
                                    appointment.APregistN -= 1
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
                except Exception, e:
                    print e
                    self.retjson['contents'] = '授权码不存在或已过期'
                    self.retjson['code'] = '10279'
        else:
            self.retjson['code'] = '10272'
            self.retjson['contents'] = r'用户认证失败'
     
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
