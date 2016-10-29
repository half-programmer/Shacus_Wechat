# coding=utf-8

'''
@author：兰威
@time :2016.9.6
'''
import json

from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Course.Coursemodel import Coursemodel
from Userinfo import Ufuncs

class Chomepage(BaseHandler):# 教程首页
    retjson ={ "code": '','contents':''}

    def post(self):
        ret_contents = {}
        ret_course = []
        ret_tag = []
        u_id = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id,u_authkey):
            type = self.get_argument('type')
            if type == '11001':  #查看教程首页
                try:
                    courses = self.db.query(Course).filter(Course.Cvalid ==1).order_by(desc(Course.Cscore)).limit(3).all() #通过score查出前三推荐给用户
                except Exception,e:
                    print e
                for course in courses:
                    ret_course.append(Coursemodel.Course_Model_Simply_Homepage(course))
                tags = self.db.query(CourseTag).all()
                for tag in tags:
                    ret_tag.append(Coursemodel.CourseTag_Model(tag))
                ret_contents['tag'] = ret_tag
                ret_contents['course'] = ret_course
                self.retjson['contents'] = ret_contents
                self.retjson['code'] = '11010'

            if type == '11101':    #教程首页点击more
                like = 0
                courses = self.db.query(Course).order_by(desc(Course.Cscore)).all()
                for course in courses:
                    u_cid = course.Cid
                    course = self.db.query(Course).filter(Course.Cid == u_cid).one()
                    try:
                        self.db.query(CourseLike).filter(CourseLike.CLcid == u_cid, CourseLike.CLuid == u_id,
                                                            CourseLike.CLvalid == 1).one()
                        like = 1
                    except Exception, e:
                        like = 0
                        print e
                    try:
                        u_ucourse = self.db.query(Usercourse).filter(Usercourse.UCuid == u_id,
                                                                        Usercourse.UCcid == u_cid).one()
                        ret_course.append(
                            Coursemodel.Course_Model_Simply(course, like, int(u_ucourse.UCfav),
                                                                           int(u_ucourse.UCseen)))
                    except Exception, e:
                        ret_course.append(Coursemodel.Course_Model_Simply(course, like, 0, 0))
                if courses:
                    self.retjson['contents'] = ret_course
                    self.retjson['code'] = '11110'




        else :
            self.retjson['contents'] = '用户授权码不正确'
            self.retjson['code'] = '11000'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))


