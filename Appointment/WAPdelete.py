# -*-coding:utf-8 -*-
'''
@autho
r :黄鑫晨
@type：微信的约拍详情
@datatime：2016.10.25
'''
import json
from BaseHandlerh import BaseHandler
from Database.tables import WAppointment


class WAPdelete(BaseHandler):

    retjson = {'code': '400', 'contents': 'None'}
    def get(self):

        auth = self.get_argument('auth')
        m_apid = self.get_argument('apid')
        if auth == 'fjsdkflnopwhxc1225':
            try:
                appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == m_apid).one()
                valid = appointment.WAPvalid
                if valid == 1:
                    appointment.WAPvalid = 0
                    try:
                        self.db.commit()
                        self.retjson['code'] = '200'
                        self.retjson['contents'] = u'删除成功'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '500'
                        self.retjson['contents'] = u'数据库提交失败'
                elif valid == 0:
                   self.retjson['code'] = '400'
                   self.retjson['contents'] = u'该约拍已被删除'
            except Exception,e:
                self.retjson['contents'] = u'该约拍不存在'
                self.retjson['code'] = '400'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


