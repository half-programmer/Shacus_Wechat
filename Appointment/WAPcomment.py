# -*- coding:utf-8 -*-
'''
@author:黄鑫晨
@name:约拍评论处理
@time:2016-10-24
'''
import json

import time

from BaseHandlerh import BaseHandler
from Database.tables import WApInfo, User


class APcommentHandler(BaseHandler):
    '''
    对约拍的评论进行处理
    '''
    retjson = {'code':'','contents':''}

    def commit(self):
        try:
            self.db.commit()
        except Exception,e:
            self.retjson['code'] = u'500'
            self.retjson['contents'] = u"数据库提交错误"

    def get(self):
        apid = self.get_argument("apid")  # 约拍id
        utel = self.get_argument("utel")  # 评论用户的手机号
        callback = self.get_argument("jsoncallback")
        comment = ''
        try:
            user = self.db.query(User).filter(User.Utel == utel).one()
            uid = user.Uid
            try:
                # 约拍项
                ap_info_entry = self.db.query(WApInfo).filter(WApInfo.WAIappoid == apid, WApInfo.WAIvalid == 1).one()
                try:
                    score = self.get_argument("score")  # 评分
                    try:
                        comment = self.get_argument("comment")  # 评论
                    except Exception, e:
                        self.retjson['code'] = "40001"
                        self.retjson['contents'] = u"无评论内容！"
                        print e
                    # 模特评论摄影师
                    if uid == ap_info_entry.WAImid:
                        ap_info_entry.WAIpscore = score
                        if comment:
                            ap_info_entry.WAImcomment = comment
                            ap_info_entry.WAImcommentT = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
                        self.commit()
                        self.retjson['code'] = "200"
                        self.retjson['contents'] = u"评论成功！"
                    # 摄影师评论模特
                    elif uid == ap_info_entry.WAIpid:
                        ap_info_entry.WAImscore = score
                        if comment:
                            ap_info_entry.WAIpcomment = comment
                            ap_info_entry.WAIpcommentT = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
                        self.commit()
                        self.retjson['code'] = "200"
                        self.retjson['contents'] = u"评论成功！"
                    # 用户Id不在该约拍中
                    else:
                        self.retjson['code'] = u'40002'
                        self.retjson['contents'] = u'该用户未参加此次约拍'
                except Exception, e:
                    print e
                    self.retjson['code'] = u'40003'
                    self.retjson['contents'] = u"无评分！"
            except Exception,e:
                print e
                self.retjson['code'] = u'40004'
                self.retjson['contents'] = u"该约拍还未选择约拍对象或已失效"
        except Exception, e:
            self.retjson['code'] = u'40005'
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)


