# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍详情
@datatime：2016.10.25
'''
import json

from Appointment.WAPusermodel import wechat_user_model_select_simply
from  BaseHandlerh import BaseHandler
from Database.tables import WAppointEntry, WAppointment, WApImage, User, WApInfo
from Userinfo.Usermodel import decode_base64
from WAPmodel import WAPmodel

class WAPdetail(BaseHandler):

    retjson = {'code': '400', 'contents': 'None'}
    def get(self):

        phone = self.get_argument('phone')
        m_apid = self.get_argument('apid')

        isregist = 0
        issponsor = 0
        ischoosed = 0
        wap_pic = []
        userlist = ''
        wapmodel = WAPmodel()
        try:
            user = self.db.query(User).filter(User.Utel == phone).one()
            m_id = user.Uid
            date = self.db.query(WAppointEntry).filter(WAppointEntry.WAEapid == m_apid,WAppointEntry.WAEvalid == 1).all()
            for item in date:
                if item.WAEregisterID == int(m_id):
                    isregist =1
                    break
            wap = self.db.query(WAppointment).filter(WAppointment.WAPid == m_apid,WAppointment.WAPvalid == 1).one()
            if wap.WAPsponsorid == int(m_id):
                issponsor = 1
                if wap.WAPstatus !=1 :
                    if wap.WAPtype == 0:
                        apinfo = self.db.query(WApInfo).filter(WApInfo.WAIappoid == m_apid,WApInfo.WAIpid == m_id).one()
                        r_id = apinfo.WAImid
                        user = self.db.query(User).filter(User.Uid == r_id).one()
                        userlist = wechat_user_model_select_simply(user)
                    if wap.WAPtype == 1:
                        apinfo = self.db.query(WApInfo).filter(WApInfo.WAIappoid == m_apid,
                                                               WApInfo.WAImid == m_id).one()
                        r_id = apinfo.WAIpid
                        user = self.db.query(User).filter(User.Uid == r_id).one()
                        userlist = wechat_user_model_select_simply(user)
            wap_picturls = self.db.query(WApImage).filter(WApImage.WAPIapid == m_apid).all()
            for pic in wap_picturls:
                wap_pic.append(pic.WAPIurl)
            type = wap.WAPtype
            if type == 0:
                apinfo = self.db.query(WApInfo).filter(WApInfo.WAImid == m_id,
                                                            WApInfo.WAIappoid == m_apid).all()
                if apinfo:
                    ischoosed = 1
                    for apinfos in apinfo :
                        r_id = apinfos.WAIpid
                        user = self.db.query(User).filter(User.Uid == r_id).one()
                        userlist = wechat_user_model_select_simply(user)
            if type == 1:
                apinfo = self.db.query(WApInfo).filter(WApInfo.WAIpid == m_id,
                                                       WApInfo.WAIappoid == m_apid).all()
                if apinfo:
                    ischoosed = 1
                    for apinfos in apinfo:
                        r_id = apinfos.WAImid
                        user = self.db.query(User).filter(User.Uid == r_id).one()
                        userlist = wechat_user_model_select_simply(user)
            retdate = wapmodel.wap_model_mutiple(wap,wap_pic,issponsor,isregist,ischoosed,userlist)
            self.retjson['contents'] = retdate
            self.retjson['code'] = '10401'
        except Exception,e:
            print e
            self.retjson['contents'] = "该活动无效"
            self.retjson['code'] = '10400'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)

