# -*- coding:utf-8 -*-
import json

from BaseHandlerh import BaseHandler
from Database.tables import NewChoosed, User


class NewChoosedHandler(BaseHandler):
    retjson = {'code': '', 'choosed': '', 'contents': ''}
    def get(self):
        callback = self.get_argument("jsoncallback")
        utel = self.get_argument('phone')
        try:
            user = self.db.query(User).filter(User.Utel == utel).one()
            new_choosed = 0
            try:
                new_choosed_entry = self.db.query(NewChoosed).filter(NewChoosed.uid == user.Uid).one()
                new_choosed = new_choosed_entry.choosed
                self.retjson['code'] = '20001'
                self.retjson['contents'] = u'成功'
            except Exception, e:
               #  如果没有这项则插入
                new_choosed_entry = NewChoosed(
                uid=user.Uid,
                choosed=0
                )
                self.db.merge(new_choosed_entry)
                try:
                    self.db.commit()
                    self.retjson['code'] = '40002'
                    self.retjson['contents'] = u'数据库无该用户约拍对象表，已更新'
                except Exception, e:
                    self.retjson['code'] = '500'
                    self.retjson['contents'] = u'数据库提交失败'

            self.retjson['choosed'] = int(new_choosed)
        except Exception, e:
            self.retjson['code'] = '40001'
            self.retjson['contents'] = "该用户不存在"
        callback = self.get_argument("jsoncallback")
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)
