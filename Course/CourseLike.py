# coding=utf-8
'''对教程关注
@author：兰威
'''
import json

from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


class Courselike(BaseHandler):
    retjson = {'code':'','contents':''}

    def post(self):
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_authkey):
            type = self.get_argument('type')
            c_id = self.get_argument('cid')
            c_exist = self.db.query(Course).filter(Course.Cid == c_id).one()
            if c_exist.Cvalid == 1:  #该教程仍然有效
                try:
                    exist = self.db.query(CourseLike).filter(CourseLike.CLcid == c_id, CourseLike.CLuid == u_id
                                                             ).one()
                    if exist.CLvalid == 1:
                        if type == '11003':  #点赞时已经点过了
                            self.retjson['code'] = '11031'
                            self.retjson['contents'] = '你已经对此活动点过赞了'
                        if type =='11004':   #取消赞时点过赞了
                            exist.CLvalid =0
                            self.retjson['code'] = '11041'
                            self.retjson['contents'] = '取消赞成功'
                            self.db.query(Course).filter(Course.Cid == c_id). \
                                update({Course.ClikeN: Course.ClikeN - 1,Course.Cscore :Course.Cscore-5}, synchronize_session=False)
                            self.db.commit()
                    else:
                        if type =='11003': #点赞时已经取消赞
                            exist.CLvalid = 1
                            self.retjson['code'] = '11032'
                            self.retjson['contents'] = '成功点赞'
                            self.db.query(Course).filter(Course.Cid == c_id). \
                                update({Course.ClikeN: Course.ClikeN + 1,Course.Cscore :Course.Cscore+5}, synchronize_session=False)
                            self.db.commit()
                        if type == '11004': #取消时已取消赞
                            self.retjson['code'] = '11042'
                            self.retjson['contents'] = '你已经对此活动取消过赞了'
                except Exception, e:
                    print e
                    if type =='11003':     #点赞时从未点过
                        entry = CourseLike(
                            CLcid=c_id,
                            CLuid=u_id,
                            CLvalid=1
                        )
                        self.db.merge(entry)
                        self.retjson['code'] = '11032'
                        self.retjson['contents'] = '成功点赞'
                        self.db.query(Course).filter(Course.Cid == c_id). \
                            update({Course.ClikeN: Course.ClikeN + 1,Course.Cscore :Course.Cscore+5}, synchronize_session=False)
                        self.db.commit()
                    if type == '11004':     #取消赞时从未点赞过
                        self.retjson['code'] = '11043'
                        self.retjson['contents'] = '你从来没有赞过这个教程'
            else :
                self.retjson['code'] = '11033'
                self.retjson['contents'] = '该教程已经失效'

        else:
            self.retjson['code'] = '11000'
            self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))