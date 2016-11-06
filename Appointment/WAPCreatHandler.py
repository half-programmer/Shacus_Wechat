# -*- coding:utf-8 -*-
'''
   @兰威
   @datatime：2016.10.09
   @type：微信创建约拍
'''
import json
import sys

from Database.tables import WAppointment, User

sys.path.append("..")
from BaseHandlerh import BaseHandler
from Wechatserver.Wpichandler import Wpichandler
from FileHandler.ImageHandler import ImageHandler
class WAPCreatHandler(BaseHandler):

    retjson = {'code':'','contents':''}

    def get(self):
        '''

        注释为post请求写法
        Returns:

        '''
        W_title = self.get_argument('title') #约拍标题
        W_type = self.get_argument('type') #约拍类型 0为约模特，1为摄影师
        W_price = self.get_argument('price')
        W_time = self.get_argument("time")
        W_location = self.get_argument('location')
        W_content = self.get_argument('content')
        W_mediaIds = self.get_arguments('serverIds[]',strip=True)
        W_phone = self.get_argument('phone')
        W_uid = self.db.query(User).filter(User.Utel == W_phone).one()
        #W_mediaIds = self.get_argument('serverIds')
        #print("我是一条漂亮的分割线————————————————————————————")
        #print W_mediaIds

        try:
            appointment = self.db.query(WAppointment).filter(WAppointment.WAPtitle == W_title,WAppointment.WAPcontent == W_content,WAppointment.WAPvalid == 1).one()
            if appointment:
                self.retjson['code'] = '10201'
                self.retjson['contents'] = r'该约拍已存在'
        except Exception, e:
            print e
            self.retjson['code'] = '10200'
            new_appointment = WAppointment(
                WAPtitle=W_title,
                WAPtype=W_type,
                WAPlocation=W_location,
                WAPcontent=W_content,  # 活动介绍
                WAPfree=W_price,
                WAPtime=W_time,
                WAPvalid=0,
                WAPstatus=1,
                WAPsponsorid=W_uid.Uid,
            )
            self.db.merge(new_appointment)
            try:
                 self.db.commit()
                 wpicture = Wpichandler()
                 image = ImageHandler()
                 Wap = self.db.query(WAppointment).filter(WAppointment.WAPtitle == W_title,WAppointment.WAPcontent == W_content).all()
                 for wap in Wap:
                     W_apid = wap.WAPid
                     image.insert_wappointment_image(W_mediaIds, W_apid)
                     wap.WAPvalid = 1
                     self.db.commit()
                     break
                 self.retjson['contents'] = '创建约拍成功'

            except Exception,e:
                print e
                self.db.rollback()
                self.retjson['code'] = '10202'
                self.retjson['contents'] = '服务器错误'
                #callback = self.get_argument("jsoncallback")
                #jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
