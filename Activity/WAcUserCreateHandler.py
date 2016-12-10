# coding=utf-8
import json

from Activity.AcAuthHandler import AcAuthHandler
from Database.tables import WAcAuth, WActivity, User
from FileHandler.ImageHandler import ImageHandler
from Wechatserver.Wpichandler import Wpichandler

'''
@author:wjl
2016.12.8 创建活动

'''

from BaseHandlerh import BaseHandler




class AcUserCreateHandler(BaseHandler):  # 创建活动
    retjson = {'code': '10310', 'contents': 'None'}

    def get(self):
            W_mediaIds = self.get_arguments('serverIds[]', strip=True)
            location = self.get_argument('location')
            title = self.get_argument('title')
            startT = self.get_argument('startT')
            endT = self.get_argument('endT')
            joinT = self.get_argument('joinT')  # 报名截止时间
            content = self.get_argument('content')  # 活动介绍

            price = self.get_argument('price')
            minp = self.get_argument('minp')#最小报名人数
            maxp = self.get_argument('maxp')#最大报名人数
            phone = self.get_argument('phone')
            WACusercontact = self.get_argument('usercontact')
            try:
                finduserid = self.db.query(User).filter(User.Utel == phone).one()


                try:
                    activity = self.db.query(WActivity).filter(WActivity.WACtitle == title, WActivity.WACcontent == content).one()

                    if activity:
                        self.retjson['code'] = '10311'
                        self.retjson['contents'] = r'该约拍已存在'
                except Exception,e:

                    print e
                    finduserid = self.db.query(User).filter(User.Utel == phone).one()
                    userid = finduserid.Uid
                    new_activity = WActivity(

                            WACsponsorid=userid,
                            WAClocation=location,
                            WACtitle=title,
                            WACstartT=startT,
                            WACendT=endT,
                            WACjoinT=joinT,
                            WACcontent=content,

                            WACprice=price,
                            WACclosed=0,
                            WACmaxp=maxp,
                            WACminp=minp,
                            WACstatus=1,
                            WACusercontact=WACusercontact,
                            )
                    self.db.merge(new_activity)
                    try:
                        self.db.commit()
                        wpicture = Wpichandler()
                        image = ImageHandler()
                        Wac = self.db.query(WActivity).filter(WActivity.WACtitle == title, WActivity.WACcontent == content).all()
                        for wac in Wac:
                            W_acid = wac.WACid
                            image.insert_activity_image(W_mediaIds,W_acid)
                            wac.WACvalid = 0
                            self.db.commit()
                            break
                        self.retjson['code']='10312'
                        self.retjson['contents'] = '创建约拍成功'

                    except Exception, e:
                        print e
                        self.db.rollback()
                        self.retjson['code'] = '10202'
                        self.retjson['contents'] = '服务器错误'
            except Exception, e:
                print e
                print '未找到该用户'
                self.retjson['code'] = '10313'
                self.retjson['contents'] = '用户未找到'
            self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
