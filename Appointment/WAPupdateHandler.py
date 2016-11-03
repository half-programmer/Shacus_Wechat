# -*- coding:utf-8 -*-
'''
   @黄鑫晨
   @datatime：2016.11.2
   @type：约拍更新信息
'''
import json
import sys

from Database.tables import WAppointment, User

sys.path.append("..")
from BaseHandlerh import BaseHandler
from Wechatserver.Wpichandler import Wpichandler
from FileHandler.ImageHandler import ImageHandler

class WAPUpdateHandler(BaseHandler):

    retjson = {'code':'','contents':''}

    def commit(self):
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            self.retjson['code'] = u'500'
            self.retjson['contents'] = u"数据库提交错误"

    def get(self):
        apid = self.get_argument('apid')
        W_content = self.get_argument('content')
        W_mediaIds = self.get_arguments('serverIds[]', strip=True)
        W_phone = self.get_argument('phone')
        try:
            user = self.db.query(User).filter(User.Utel == W_phone).one()
            try:
                appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == apid,
                                                             WAppointment.WAPvalid == 1).one()
                if appointment:
                    if appointment.WAPsponsorid == user.Uid:
                        appointment.WAPcontent = W_content,  # 活动介绍
                        self.commit()
                        try:
                            self.db.commit()
                            wpicture = Wpichandler()
                            image = ImageHandler()
                            # 找到要修改的约拍
                            image.insert_wappointment_image(W_mediaIds, apid)
                            self.retjson['code'] = 200
                            self.retjson['contents'] = '修改约拍成功'
                            self.commit()
                        except Exception, e:
                            print e
                            self.retjson['code'] = '40003'
                            self.retjson['contents'] = '图片上传错误'
                    else:
                        self.retjson['code'] = '40002'
                        self.retjson['contents'] = u"您不是约拍发起者，没有修改权限"
            except Exception, e:
                print e
                self.retjson['code'] = '40001'
                self.retjson['contents'] = u'该约拍已失效'
        except Exception:
            self.retjson['code'] = '40004'
            self.retjson['contents'] = u"该用户不存在"

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
