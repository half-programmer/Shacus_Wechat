# -*-coding:utf-8 -*-
'''
@autho
r :黄鑫晨
@type：用户删除约拍
@datatime：2016.10.25
'''
import json
from BaseHandlerh import BaseHandler
from Database.tables import WAppointment, User, WAppointEntry


class WAPdelete(BaseHandler):

    retjson = {'code': '400', 'contents': 'None'}

    def commit(self):
        try:
            self.db.commit()
        except Exception,e:
            self.db.rollback()
            self.retjson['code'] = u'500'
            self.retjson['contents'] = u"数据库提交错误"

    def get(self):

        utel = self.get_argument('utel')
        apid = self.get_argument('apid')
        try:
            user = self.db.query(User).filter(User.Utel == utel).one()
            try:
                appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == apid).one()
                # 1为发布中，2为已确定约拍对象(进行中) 3为一方已结束 4为两方都结束
                status = appointment.WAPstatus
                valid = appointment.WAPvalid
                if valid == 1:
                    # 发布中
                    if status == 1:
                        try:
                            self.retjson['code'] = '40004'
                            self.retjson['contents'] = u'该约拍已有人报名，不能删除'
                            registers = self.db.query(WAppointEntry).filter(WAppointEntry.WAEapid == apid).all()

                        # 没有人报名
                        except Exception, e:
                            print e
                            appointment.WAPvalid = 0
                            self.retjson['code'] = '200'
                            self.retjson['contents'] = u'删除成功'
                            self.commit()
                    else:
                        self.retjson['code'] = '40005'
                        self.retjson['contents'] = u'只有报名阶段的约拍才可以被删除'
                elif valid == 0:
                   self.retjson['code'] = '40003'
                   self.retjson['contents'] = u'该约拍已被删除'
            except Exception, e:
                self.retjson['contents'] = u'该约拍不存在'
                self.retjson['code'] = '40002'
        except Exception, e:
            self.retjson['contents'] = u'该用户不存在'
            self.retjson['code'] = '40001'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


