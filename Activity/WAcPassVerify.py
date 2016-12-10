#-*- coding:utf-8 -*-
from BaseHandlerh import BaseHandler
from Database.tables import WActivity
from messsage import passVerifymessage
import json

class WAcPassVerify(BaseHandler):
    retjson={'code':'200','content':'none'}
    def get(self):
        acid = self.get_argument('WAcid')
        usercontact = self.get_argument("usercontact")
        try:
            acinfo= self.db.query(WActivity).filter(WActivity.WACid== acid).one()
            acinfo.WACvalid = 1
            self.db.commit()
            #passVerifymessage(usercontact,acinfo.WACusercontact)
            self.retjson['code']='10330'
            self.retjson['content'] = '审核成功！'
        except Exception,e:
            print e
            print '查找活动出现错误'
            self.retjson['code']='10331'
            self.retjson['content']="查找活动出现错误"
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)

