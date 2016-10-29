# coding=utf-8
import json

from tornado.escape import json_encode

from BaseHandlerh import BaseHandler
from Database.tables import WActivity, WAcImage, User, WAcEntry
from FileHandler.Upload import AuthKeyHandler

'''
@author:黄鑫晨
@2016-10-11
@返回活动详细信息
'''


def md5(str):
    import base64
    m = base64.encodestring(str)
    return m



class AcInfoHandler(BaseHandler):
    retjson = {}

    def get(self):
        acid = self.get_argument('acid')  # 活动id
        m_phone = self.get_argument('phone') #用户手机


        isregist = 0
        try:
            userinfo = self.db.query(User).filter(User.Utel == m_phone).one()  # 判断是否报名
            userid = userinfo.Uid

            try:
                acregist = self.db.query(WAcEntry).filter(
                    WAcEntry.WACEacid == acid , WAcEntry.WACEregisterid == userid).one()
                if acregist.WACEregistvalid == 1:
                    isregist = 1
                elif acregist.WACEregistvalid == 0:
                    isregist = 0
            except Exception, e:
                isregist = 0
                print "没有报名"
        except Exception,e:
            print e




        # 判断是否有权限
        auth  = AuthKeyHandler()

        try:
            exist = self.db.query(WActivity).filter(WActivity.WACid == acid, WActivity.WACvalid == 1).one()
            # 该活动存在
            if exist:
                picurls = []
                pics = self.db.query(WAcImage).filter(WAcImage.WACIacid == acid).all()
                for pic in pics:
                    picurls.append(auth.download_url(pic.WACIurl))



                activity = dict(
                    code=200,
                    id=exist.WACid,
                    sponsorid=exist.WACsponsorid,
                    isregist = isregist,
                    location=exist.WAClocation,
                    title=exist.WACtitle,
                    startT=exist.WACstartT.strftime('%Y-%m-%d'),
                    endT=exist.WACendT.strftime('%Y-%m-%d'),
                    joinT=exist.WACjoinT.strftime('%Y-%m-%d'),
                    content=exist.WACcontent,
                    free=exist.WACfree,
                    price=exist.WACprice,
                    closed=exist.WACclosed,
                    createT=exist.WACcreateT.strftime('%Y-%m-%d'),
                    maxp=exist.WACmaxp,
                    minp=exist.WACminp,
                    registN=exist.WACregistN,
                    status=exist.WACstatus,
                    picurls=picurls,
                )
                self.retjson = activity
        except Exception, e:
            print e
            self.retjson['contents'] = dict(
                code=402,
                content='该活动不存在或已失效')
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
