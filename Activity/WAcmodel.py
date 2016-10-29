# coding=utf-8
from Database.tables import UserImage, Image,WActivity, WAcImage
from FileHandler.Upload import AuthKeyHandler
from Database.models import get_db
'''
@author:王佳镭
'''
class ACmodelHandler:
    @classmethod
    def ac_Model_simply(clas,activity,retdata):
        '''得到简单活动模型
        :return:  retjson
        '''
        auth = AuthKeyHandler()
        #get activityimg
        aclurl = get_db().query(WAcImage).filter(WAcImage.WACIacid == activity.WACid).all()
        Acurl = auth.download_url(aclurl[0].WACIurl)
        ac_simply_info = dict(
        WACid=activity.WACid,
        WACtitle=activity.WACtitle,
        Wacstatus = activity.WACstatus,
        WACimgurl= Acurl,
        WACcontent=activity.WACcontent[0:12],
        )
        return ac_simply_info
