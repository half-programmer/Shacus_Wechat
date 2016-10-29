# coding=utf-8
'''
对教程进行收藏
@author：兰威
'''
import json

from BaseHandlerh import BaseHandler
from Userinfo import Ufuncs


class Coursefav(BaseHandler):

    retjson = {'code': '', 'contents': ''}

    def post(self):
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        c_id =self.get_argument('cid')
        ufuncs = Ufuncs.Ufuncs()
        type = self.get_argument('type')
        if ufuncs.judge_user_valid(u_id, u_authkey):
            try:
                self.db.query(Course).filter(Course.Cid == c_id,Course.Cvalid ==1).one()
                try:
                    exist = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id,Usercourse.UCcid == c_id).one()
                    if type == '11008':     #用户收藏教程
                        if exist.UCfav == 1:#用户收藏过此教程
                            self.retjson['contents'] = '你已经收藏过次教程'
                            self.retjson['code'] = '11084'
                        else:              #用户没有收藏过此教程
                            exist.UCfav = 1
                            self.db.query(Course).filter(Course.Cid == c_id). \
                                update({Course.CfavN: Course.CfavN + 1,Course.Cscore :Course.Cscore+10}, synchronize_session=False)
                            try:
                                self.db.commit()
                                self.retjson['contents'] = '收藏教程成功'
                                self.retjson['code'] = '11083'
                            except Exception,e:
                                self.retjson['contents'] = '服务器出错'
                                self.retjson['code'] = '11082'
                    if type =='11009':    #用户取消收藏教程
                        if exist.UCfav == 1:  #用户取消收藏教程
                            exist.UCfav = 0
                            self.db.query(Course).filter(Course.Cid == c_id). \
                                update({Course.CfavN: Course.CfavN - 1,Course.Cscore :Course.Cscore-10}, synchronize_session=False)
                            try:
                                self.db.commit()
                                self.retjson['contents'] = '取消收藏教程成功'
                                self.retjson['code'] = '11092'
                            except Exception, e:
                                self.retjson['contents'] = '服务器出错'
                                self.retjson['code'] = '11082'
                        else :            #用户已经取消收藏此教程
                            self.retjson['contents'] = '你已经取消收藏过次教程'
                            self.retjson['code'] = '11093'

                except Exception,e:
                    if type =='11008':    #用户从来没有对此教程进行过任何的操作
                        usercourse = Usercourse(
                             UCuid = u_id,
                             UCcid = c_id,
                             UCseen = 0,
                             UCfav =1
                         )
                        self.db.merge(usercourse)
                        self.db.query(Course).filter(Course.Cid == c_id).\
                            update({Course.CfavN: Course.CfavN+1,Course.Cscore :Course.Cscore+10},synchronize_session=False)
                        try:
                            self.db.commit()
                            self.retjson['contents'] = '收藏教程成功'
                            self.retjson['code'] = '11083'
                        except Exception,e:
                            self.db.rollback()
                            self.retjson['contents'] = '服务器出错'
                            self.retjson['code'] = '11082'
                    if type == '11009':      #用户对该教程没有进行过任何的操作却要取消收藏
                        self.retjson['contents'] = '你没有收藏过次教程'
                        self.retjson['code'] = '11091'
            except Exception,e:
                self.retjson['contents'] = '该教程无效'
                self.retjson['code'] = '11081'
        else :
            self.retjson['code'] = '11080'
            self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
