
# coding=utf-8
'''
@author: 黄鑫晨
'''
from  BaseHandlerh import BaseHandler
def commit(self,retjson):
    try:
        self.db.commit()  #  retjson默认为成功情况内容
    except:
        self.db.rollback()
        retjson['code'] = 408  # Request Timeout
        retjson['content'] = 'Some errors when commit to database, please try again'