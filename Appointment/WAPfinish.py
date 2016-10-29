# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍取消报名
@datatime：2016.10.27
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, WApInfo, WApFinish, WAppointment


class WAPfinish(BaseHandler):

    retjson = {'code': '400', 'contents': 'None'}
    def get(self):

        phone = self.get_argument("phone")
        ap_id = self.get_argument('apid')

        user = self.db.query(User).filter(User.Utel == phone).one()
        u_id = user.Uid
        ap = self.db.query(WAppointment).filter(WAppointment.WAPid == ap_id).one()
        if ap.WAPstatus == 1:
            self.retjson['code'] = '10302'
            self.retjson['contents'] = '不能结束'
        else:
            exist = self.db.query(WApInfo).filter(WApInfo.WAIappoid == ap_id).one()
            if exist.WAImid == u_id or exist.WAIpid == u_id:
                try:
                    exist = self.db.query(WApFinish).filter(WApFinish.WAFapid == ap_id,WApFinish.WAFuid == u_id).one()
                    self.retjson['code'] = '10301'
                    self.retjson['contents'] = '已结束此约拍'
                except Exception,e:
                    new_item = WApFinish(
                        WAFapid=ap_id,
                        WAFuid = u_id
                      )
                    self.db.merge(new_item)
                    ap.WAPstatus+=1
                    self.db.commit()
                    self.retjson['code'] = '10303'
                    self.retjson['contents'] = '结束成功'
            else:
                self.retjson['code'] = '10300'
                self.retjson['contents'] = '未参加此约拍'
            callback = self.get_argument("jsoncallback")
            jsonp = "{jsfunc}({json});".format(jsfunc=callback,json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
            self.write(jsonp)

