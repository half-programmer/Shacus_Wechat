#-*-coding:utf-8 -*-

import json
from Activity.WAcmodel import ACmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import WActivity
from datetime import datetime

class WAcVerify(BaseHandler): #审核活动的列表
    retjson={'code':'10320','content':'none'}
    def get(self):
        dnow=datetime.now()
        try:
            data=self.db.query(WActivity).filter(WActivity.WACvalid==0,WActivity.WACendT>dnow).all()
            retdata=[]
            for item in data:
                retdata01 = ACmodelHandler.ac_Model_simply(item, retdata)
                self.retjson['code'] = '10303'
                retdata.append(retdata01)
                self.retjson['contents'] = retdata
        except Exception, e:
            print e
            self.retjson['code'] = '10304'
            self.retjson['contents'] = 'there is no activity'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
