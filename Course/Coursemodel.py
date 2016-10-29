# coding=utf-8
'''返回不同格式的教程模型
@author：兰威
'''

from FileHandler.Upload import AuthKeyHandler
class Coursemodel(object):

    @classmethod
    def Course_Model_Simply_Homepage(clas, course): # 首页推荐的三个教程
        auth = AuthKeyHandler()
        ret_course = dict(
            Cid = course.Cid,
            Ctitle = course.Ctitle,
            CimageUrl  =  auth.download_url(course.Cimagerul),
            Curl = course.Curl
        )
        return ret_course

    @classmethod
    def CourseTag_Model(clas,Tag):
        auth = AuthKeyHandler()
        ret_tag = dict(
            CTid = Tag.CTid,
            CTname = Tag.CTname,
            CThint = Tag.CThint,
            CTcourseN = Tag.CTcourseN,
            CTimageurl = auth.download_url(Tag.CTimageurl)
        )
        return ret_tag

    @classmethod
    def Course_Model_Complete(cls,course,tags):
        auth = AuthKeyHandler()
        ret_course = dict(
            Cid=course.Cid,
            Ctitle=course.Ctitle,
            CimageUrl=auth.download_url(course.Cimagerul),
            Curl = course.Curl,
            ClikeN = course.ClikeN,
            CwatchN = course.CwatchN,
            CfavN = course.CfavN,
            Cscore = course.Cscore,
            CTags = tags
        )
        return ret_course

    @classmethod
    def Course_Model_Simply(cls,course,like,fav,see):
        auth = AuthKeyHandler()
        ret_course = dict(
            Cid=course.Cid,
            Ctitle=course.Ctitle,
            CimageUrl=auth.download_url(course.Cimagerul),
            Cvalid = int(course.Cvalid),
            CwatchN = course.CwatchN,
            CfavN = course.CfavN,
            Cliked = like,
            Cfav = fav,
            Csee = see
        )
        return ret_course

