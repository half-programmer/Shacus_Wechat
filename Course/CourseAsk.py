# coding=utf-8
'''返回不同格式的教程模型
@author：兰威
'''
import json

from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Course import Coursemodel
from Userinfo import Ufuncs


class CourseAsk(BaseHandler):
    retjson ={'code':'','contents':''}
    def post(self):
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_authkey):
            type = self.get_argument('type')

            if type =='11002':    #请求教程的详细信息
                c_id = self.get_argument('cid')
                tags = []
                ret_content ={}
                try:
                    self.db.query(Course).filter(Course.Cid ==c_id , Course.Cvalid == 1).one()
                    try:
                        exist = self.db.query(Usercourse).filter(Usercourse.UCcid == c_id,Usercourse.UCuid == u_id).one() #判断是否曾经看过此教程
                        if exist.UCseen == 0 :
                            exist.UCseen =1
                            self.db.commit()
                    except Exception,e:
                        entry = Usercourse(
                            UCuid = u_id,
                            UCcid = c_id,
                            UCseen =1,
                            UCfav =0
                        )
                        self.db.merge(entry)
                        self.db.commit()


                    course = self.db.query(Course).filter(Course.Cid == c_id).one()
                    entrys = self.db.query(CourseTagEntry).filter(CourseTagEntry.CTEcid == c_id,
                                                                CourseTagEntry.CTEvalid == 1).all()         #查询教程的标签
                    for entry in entrys:
                        tag_info = self.db.query(CourseTag).filter(CourseTag.CTid == entry.CTEtid).one()
                        tags.append(tag_info.CTname)
                    ret_content ['course']= Coursemodel.Coursemodel.Course_Model_Complete(course,tags)     #将浏览人数加一
                    course.CwatchN+=1
                    course.Cscore +=1
                    self.db.commit()
                    try:
                        self.db.query(CourseLike).filter(CourseLike.CLcid ==c_id,
                                                             CourseLike.CLuid == u_id,
                                                             CourseLike.CLvalid == 1).one()                 #查询是否关注过该教程
                        ret_content['isliked'] = 1
                    except Exception,e:
                        ret_content['isliked'] = 0

                    self.retjson['code'] = '11021'
                    self.retjson['contents'] = ret_content
                except Exception,e:
                    self.retjson['code'] = '11022'
                    self.retjson['contents'] = '该教程无效'

            if type == '11005':  # 返回我看过的所有教程
                ret_course =[]
                like = 0
                u_courses = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id,Usercourse.UCseen == 1).all()
                for u_course in u_courses:
                    u_cid = u_course.UCcid
                    course = self.db.query(Course).filter(Course.Cid == u_cid).one()
                    fav = u_course.UCfav
                    try:
                        self.db.query(CourseLike).filter(CourseLike.CLcid == u_cid,CourseLike.CLuid == u_id,
                                                     CourseLike.CLvalid == 1 ).one()
                        like =1
                    except Exception,e:
                        print e
                    ret_course.append(Coursemodel.Coursemodel.Course_Model_Simply(course,like,int(fav),1))
                self.retjson['contents'] = ret_course
                self.retjson['code'] = '11051'

            if type =='11006':   #返回我收藏的所有教程
                ret_course = []
                like = 0
                u_courses = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id, Usercourse.UCfav == 1).all()
                for u_course in u_courses:
                    u_cid = u_course.UCcid
                    course = self.db.query(Course).filter(Course.Cid == u_cid).one()
                    see = u_course.UCseen
                    try:
                        self.db.query(CourseLike).filter(CourseLike.CLcid == u_cid, CourseLike.CLuid == u_id,
                                                         CourseLike.CLvalid == 1).one()
                        like = 1
                    except Exception, e:
                        print e
                    ret_course.append(Coursemodel.Coursemodel.Course_Model_Simply(course, like, 1, int(see)))
                self.retjson['contents'] = ret_course
                self.retjson['code'] = '11061'

            if type == '11007':   #根据标签返回相应课程
                tag_id = self.get_argument('tid')
                like = 0
                ret_course = []
                courses = self.db.query(CourseTagEntry).filter(CourseTagEntry.CTEtid == tag_id).\
                    order_by(desc(CourseTagEntry.CTEcreateT)).all()
                for course in courses:
                    u_cid = course.CTEcid
                    course = self.db.query(Course).filter(Course.Cid == u_cid).one()
                    try:
                        self.db.query(CourseLike).filter(CourseLike.CLcid == u_cid, CourseLike.CLuid == u_id,
                                                         CourseLike.CLvalid == 1).one()
                        like = 1
                    except Exception, e:
                        print e
                    try:
                        u_ucourse = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id,Usercourse.UCcid ==u_cid ).one()
                        ret_course.append(Coursemodel.Coursemodel.Course_Model_Simply(course, like, int(u_ucourse.UCfav), int(u_ucourse.UCseen)))
                    except Exception,e:
                        ret_course.append(Coursemodel.Coursemodel.Course_Model_Simply(course, like, 0,0))
                if courses :
                    self.retjson['contents'] = ret_course
                    self.retjson['code'] = '11071'
                else :
                    self.retjson['contents'] = '没有更多了'
                    self.retjson['code'] = '11072'
        else :
            self.retjson['code']  ='11000'
            self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))