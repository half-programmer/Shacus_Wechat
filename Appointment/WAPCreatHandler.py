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
        W_uid = self.db.query(User).filter(User.Utel == W_phone ).one()
        #W_mediaIds = self.get_argument('serverIds')
        #print("我是一条漂亮的分割线————————————————————————————")
        #print W_mediaIds

        try:
            appointment = self.db.query(WAppointment).filter(WAppointment.WAPtitle == W_title).one()
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
                WAPsponsorid=W_uid,
            )
            self.db.merge(new_appointment)
            try:
                self.db.commit()
            except Exception,e:
                self.db.roolback()
                self.retjson['code'] = '10202'
                self.retjson['contents'] = '服务器错误'
            wpicture = Wpichandler()
            image = ImageHandler()
            Wap = self.db.query(WAppointment).filter(WAppointment.WAPtitle == W_title).one()
            W_apid = Wap.WAPid
            #mediaids = json.loads(W_mediaIds)
            if wpicture.pichandler(W_mediaIds,W_mediaIds):
                #image.insert_wappointment_image(mediaids,W_apid)
                image.insert_wappointment_image(W_mediaIds, W_apid)
                Wap.WAPvalid = 1
                self.db.commit()
            self.retjson['contents'] = '创建约拍成功'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
