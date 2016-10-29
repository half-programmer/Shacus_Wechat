# coding=utf-8
import base64
import json

from Database.tables import UserImage, Image,WActivity, WAcImage, User, WAcEntry
from BaseHandlerh import BaseHandler
'''
@author:王佳镭
'''
class WAquitcregist(BaseHandler):
    retjson= {'code':'200','contents':'null'}
    def get(self):
        m_wacid = self.get_argument('wacid',default='null')
        m_phone = self.get_argument('phone',default='null')

        try:
            userinfo = self.db.query(User).filter(User.Utel==m_phone).one()
            userid = userinfo.Uid
            try:
                acregist = self.db.query(WAcEntry).filter(WAcEntry.WACEacid == m_wacid , WAcEntry.WACEregisterid == userid).one()
                if acregist:
                    if acregist.WACEregistvalid == 0:
                        self.retjson['code'] = '10309'
                        self.retjson['contents'] = '没有报名'
                    elif acregist.WACEregistvalid == 1:
                        acregist.WACEregistvalid = 0
                        no = self.db.query(WActivity).filter(acregist.WACEacid == WActivity.WACid).all()
                        no[0].WACregistN -=1
                        self.db.commit()
                        self.db.commit()
                        self.retjson['code']  = '10310'
                        self.retjson['contents']= '取消报名成功'
            except Exception,e:
                print e
                self.retjson['code']='10311'
                self.retjson['contents']='没有报名02'

        except Exception,e:
            print e
            self.retjson['contents'] = '10308'
            self.retjson['contents'] = '没有此用户'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
