# coding=utf-8
'''
  @author:黄鑫晨
  2016.08.29   2016.09.03
'''
import json

from sqlalchemy import desc

import Userinfo
from APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


class APaskHandler(BaseHandler):  # 请求约拍相关信息

    # todo:返回特定条件下的约拍
    retjson = {'code': '', 'contents': ''}

    def refresh_list(self, type, offset_apid, u_id):
        retdata = []
        try:
            #attention:< ，因为返回新的
            appointments = self.db.query(Appointment). \
                filter(Appointment.APtype == type, Appointment.APclosed == 0, Appointment.APvalid == 1,
                       Appointment.APstatus != 2,
                       Appointment.APid < offset_apid).from_self().order_by(desc(Appointment.APcreateT)). \
                limit(6).all()
            if appointments:
                APmodelHandler.ap_Model_simply(appointments, retdata, u_id)
                self.retjson['code'] = '10253'  # 刷新成功，返回6个
                self.retjson['contents'] = retdata
            else:
                print appointments.first().APtype
        except Exception, e:  # 剩余约拍不足6个，返回剩余全部约拍
            print e
            try:
                appointments = self.db.query(Appointment). \
                    filter(Appointment.APtype == type, Appointment.APclosed == 0, Appointment.APvalid == 1,
                           Appointment.APstatus != 2,
                           Appointment.APid < offset_apid).order_by(desc(Appointment.APcreateT)). \
                    all()
                if appointments:
                    APmodelHandler.ap_Model_simply(appointments, retdata, u_id)
                    self.retjson['code'] = '10263'  # 剩余约拍不足6个，返回剩余全部约拍
                    self.retjson['contents'] = retdata
                else:
                    self.retjson['code'] = '10262'
                    self.retjson['contents'] = r"没有更多约拍"
            except Exception, e:
                self.retjson['code'] = '10262'
                self.retjson['contents'] = r"没有更多约拍"

    def no_result_found(self, e):
        print e
        self.retjson['code'] = '10261'
        self.retjson['contents'] = '未查询到约拍记录'

    def get_ap_Model_from_aeids(self, appoint_entrys):
         ap_ids = []
         for ap_entry in appoint_entrys:
            ap_id = ap_entry.AEapid
            ap_ids.append(ap_id)
         return self.get_ap_Model_from_apids(ap_ids)

    def get_ap_Model_from_apids(self, apids):
        appointments = []
        for apid in apids:
            appointment = self.db.query(Appointment).filter(Appointment.APid == apid).one()
            appointments.append(appointment)
        return appointments

    def ap_ask_user(self, uid, retdata):  # 查询指定用户的所有约拍
        '''
        :param user: 传入一个User对象
        :return: 无返回，直接修改retjson
        '''
        #todo:需判断该用户是否存在
        try:
            appointments1 = self.db.query(Appointment).filter(Appointment.APsponsorid == uid, Appointment.APvalid == 1).all()  # 用户自己发起的
            appointentrys = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == uid, AppointEntry.AEvalid == 1).all()  # 用户报名的

            APmodelHandler.ap_Model_simply(appointments1, retdata, uid)
            APmodelHandler.ap_Model_simply(self.get_ap_Model_from_aeids(appointentrys), retdata, uid)
            self.retjson['code'] = '10256'
            self.retjson['contents'] = retdata
        except Exception, e:
            print e
            self.no_result_found(e)

    def post(self):
        u_auth_key = self.get_argument('authkey')
        request_type = self.get_argument('type')
        u_id = self.get_argument('uid')


        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_auth_key):

            if request_type == '10231':  # 请求所有设定地点的摄影师发布的约拍中未关闭的6
                retdata = []
                try:
                    appointments = self.db.query(Appointment). \
                        filter(Appointment.APtype == 1, Appointment.APclosed == 0, Appointment.APvalid == 1,
                               Appointment.APstatus != 2).\
                        order_by(desc(Appointment.APid)).limit(6).all()
                    APmodelHandler.ap_Model_simply(appointments, retdata, u_id)
                    self.retjson['code'] = '10251'
                    self.retjson['contents'] = retdata
                except Exception, e: # 没有找到约拍
                    print e
                    self.no_result_found(e)
            elif request_type == '10235':  # 请求所有设定地点的模特发布的约拍中未关闭的
                retdata = []
                try:
                    appointments = self.db.query(Appointment). \
                        filter(Appointment.APtype == 0, Appointment.APclosed == 0, Appointment.APvalid == 1,
                               Appointment.APstatus != 2).\
                    order_by(desc(Appointment.APid)).limit(6).all()
                    APmodelHandler.ap_Model_simply(appointments, retdata, u_id)
                    self.retjson['code'] = '10252'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    self.no_result_found(e)

            elif request_type == '10240':  # 请求自己参与（包括发布）的所有约拍
                retdata = []
                self.ap_ask_user(u_id, retdata)
            elif request_type == '10241':  # 请求指定用户参与的所有约拍
                find_u_id = self.get_argument('finduid')
                retdata = []
                self.ap_ask_user(find_u_id, retdata)
            elif request_type == '10242':  # 返回约拍详情
                ap_id = self.get_argument('apid')
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()
                    if appointment:
                        response = APmodelHandler.ap_Model_multiple(appointment, u_id)
                        print 'before equal'
                        try:
                            print "in try"
                            if appointment.APsponsorid == int(u_id):
                                response['AP_issponsor'] = 1
                            else:
                                response['AP_issponsor'] = 0
                        except Exception, e:
                            print e
                        self.retjson['code'] = '10254'
                        self.retjson['contents'] = response
                except Exception, e:
                    print e
                    self.no_result_found(e)
            elif request_type == '10243':  # 刷新并拿到指定Id后的6个摄影师约拍
                offset_apid = self.get_argument('offsetapid')
                self.refresh_list(1, offset_apid, u_id)
            elif request_type == '10244':  # 刷新并拿到指定Id后的6个模特约拍
                offset_apid = self.get_argument('offsetapid')
                self.refresh_list(0, offset_apid,  u_id)
            elif request_type == '10245':  # 返回报名某约拍的全部用户列表
                ap_id = self.get_argument('apid')
                try:
                    #todo：利用join
                    appointment = self.db.query(Appointment).filter(Appointment.APid == ap_id).one()  # 查找是否有此约拍
                    if appointment:
                        print 'before equal'
                        try:
                            print "in try"
                            userids = Ufuncs.Ufuncs.get_registids_from_appointment(appointment)
                            print 'before get '
                            registers = Ufuncs.Ufuncs.get_users_chooselist_from_uids(userids, appointment.APid)
                            self.retjson['code'] = '10257'
                            self.retjson['contents'] = registers
                        except Exception, e:
                            print e
                            self.retjson['code'] = ''
                            self.retjson['contents'] = u'读写错误'

                except Exception, e:
                    print e
                    self.retjson['code'] = '10264'
                    self.retjson['contents'] = u'未查询到报名人'


        else:
            self.retjson['contents'] = '授权码不存在或已过期'
            self.retjson['code'] = '10214'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

