# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍提醒
@datatime：2016.11.20
'''
import datetime

from BaseHandlerh import BaseHandler
from Database.tables import WAppointment, WApInfo
from messsage import selectmessage


class WAPRemind(BaseHandler):

    def get(self):
        print("进入提醒阶段\n_____________")
        #查询未提醒的报名中的且有效且有人报名的约拍
        WAPs = self.db.query(WAppointment).filter(WAppointment.WAPremind == 0,WAppointment.WAPvalid == 1,
                                                  WAppointment.WAPregistN > 0,WAppointment.WAPstatus == 1).all()
        for WAP in WAPs:
            delta = datetime.datetime.now() - WAP.WAPcreateT
            #判断是否已经创建了3天
            if delta>datetime.timedelta(days=3):
                # 是否选择了用户，未选择则发送提醒短信
                # chooser = self.db.query(WApInfo).filter(WApInfo.WAIappoid == WAP.WAPid,WApInfo.WAIvalid == 1).all()
                # if not chooser:
                selectmessage('15151861978','lalala','1312312312')

