# coding=utf-8
import json

from Activity.AcAuthHandler import AcAuthHandler
from Database.tables import WAcAuth, WActivity

'''
@author:黄鑫晨
2016.10.11 创建活动
'''

from BaseHandlerh import BaseHandler

global admin_id
admin_id = 1


class AcCreateHandler(BaseHandler):  # 创建活动
    retjson = {'code': '10300', 'contents': 'None'}

    def get(self):

        auth = self.get_argument('auth')
        # 判断是否有权限
        try:
            exist = self.db.query(WAcAuth).filter(WAcAuth.WAauth == auth).one()
            # 有该认证
            if exist:
                #  已经被使用
                if exist.WAAused == 1:
                    self.retjson['code'] = '401'
                    self.retjson['contents'] = "该权限已被其他活动使用，请重新申请"
                # 未被使用，可以使用
                else:
                    # 标注为使用过
                    try:
                        location = self.get_argument('location')
                        title = self.get_argument('title')
                        startT = self.get_argument('startT')
                        endT = self.get_argument('endT')
                        joinT = self.get_argument('joinT')  # 报名截止时间
                        content = self.get_argument('content')  # 活动介绍
                        free = self.get_argument('free')
                        price = self.get_argument('price')
                        minp = self.get_argument('minp')
                        maxp = self.get_argument('maxp')
                        new_activity = WActivity(
                        WACsponsorid=admin_id,
                        WAClocation=location,
                        WACtitle=title,
                        WACstartT=startT,
                        WACendT=endT,
                        WACjoinT=joinT,
                        WACcontent=content,
                        WACfree=free,
                        WACprice=price,
                        WACclosed=0,
                        WACmaxp=maxp,
                        WACminp=minp,
                        WACstatus=1,
                        )
                        exist.WAAused = 1
                        try:
                            self.db.merge(new_activity)
                            self.db.commit()
                            self.retjson['code'] = '200'
                            self.retjson['contents'] = '发布成功'
                        except Exception, e:
                            print e
                            self.retjson['code'] = '401'
                            self.retjson['contents'] = '数据库插入失败，请重新发布'
                    except Exception, e:
                           self.retjson['code'] = '403'
                           self.retjson['contents'] = '参数填写错误'
        except Exception, e:
            print e
            self.retjson['code'] = '402'
            self.retjson['contents'] = '权限不存在，请获取权限'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
