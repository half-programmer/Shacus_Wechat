# -*- coding:utf-8 -*-
import json
import urllib
import urllib2


from Appointment.WAPmodel import WAPmodel
from BaseHandlerh import BaseHandler

# 约拍伴侣
from Database.tables import  WApCompanions, WApAuth
from FileHandler.ImageHandler import ImageHandler


class ApCompanionHandler(BaseHandler):
    retjson = {'code':'', 'contents':''}
    def get(self):
        type = self.get_argument('type')
        if type == '10900':   # 发布约拍伴侣
            auth = self.get_argument('auth')
            ApcTitle = self.get_argument('title')
            ApOrc = self.get_argument('orgnazation')
            ApcContent = self.get_argument('content')
            ApcUrl = self.get_argument('companionUrl')
            Apcimg = self.get_arguments('companionImgs[]', strip=True)
            # 判断是否有权限
            try:
                exist = self.db.query(WApAuth).filter(WApAuth.WApauth == auth).one()
                # 有该认证
                if exist:
                    #  已经被使用
                    if exist.WAAused == 1:
                        self.retjson['code'] = '401'
                        self.retjson['contents'] = "该权限已被其他活动使用，请重新申请"
                    # 未被使用，可以使用
                    else:
                        # 标注为使用过
                        new_ApCompanion = WApCompanions(
                            WAPCname=ApcTitle,
                            WAPCServeintro=ApcContent,  # 服务内容介绍
                            WAPCOrganintro=ApOrc,
                            WAPCvalid=1,
                            WAPCContact=ApcUrl,
                            )
                        self.db.merge(new_ApCompanion)
                        self.db.commit()
                        try:
                            OneCompanion = self.db.query(WApCompanions).filter(WApCompanions.WAPCname == ApcTitle,
                                                                    WApCompanions.WAPCServeintro == ApcContent,
                                                                    WApCompanions.WAPCContact == ApcUrl,
                                                                    WApCompanions.WAPCvalid == 1).one()
                            image = ImageHandler()
                            image.insert_companion_image(Apcimg, OneCompanion.WAPCid)
                            values = {
                                'type': '10900',
                                'title': ApcTitle,
                                'orgnazation': ApOrc,
                                'content': ApcContent,
                                'companionUrl': ApcUrl,
                                'companionImgs[]': Apcimg,
                            }
                            post_data=urllib.urlencode(values)
                            url = 'http://114.215.16.151:81/appointment/companion'
                            req = urllib2.Request(url, post_data)
                            response = urllib2.urlopen(req)
                            print '同步约拍伴侣成功'
                            self.db.commit()
                            self.retjson['code'] = '10900'
                            self.retjson['contents'] = '约拍伴侣创建成功'
                        except Exception, e:
                            print e
                            self.retjson['code']='10901'
                            self.retjson['contents']='创建失败'
            except Exception, e:
                    print e
                    self.retjson['code'] = '10903'
                    self.retjson['contents'] = '权限不存在，请获取权限'
        # elif type == '10902':  # 删除一个约拍伴侣
        #     Companion_id = self.get_argument('CompanionId')
        #     try:
        #         Companion_to_delete = self.db.query(ApCompanion).filter(ApCompanion.ApCompanionid == Companion_id).one()
        #         Companion_to_delete.ApCompanionValid = 0
        #         self.db.commit()
        #         self.retjson['code']='10902'
        #         self.retjson['contents']='删除成功'
        #     except Exception, e:
        #         print e
        #         self.retjson['code']='10903'
        #         self.retjson['contents']= '查找约拍伴侣失败'
        elif type == '10904':# 返回约拍伴侣
            retdata = []
            Companion_all = self.db.query(WApCompanions).filter(WApCompanions.WAPCvalid == 1).all()
            modelhandler = WAPmodel()
            for item in Companion_all:
                modelhandler.ApCompanion(item, retdata)

            self.retjson['code'] = '10904'
            self.retjson['contents'] = retdata


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))






