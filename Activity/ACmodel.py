# coding=utf-8
from Database.tables import UserImage, Image
from FileHandler.Upload import AuthKeyHandler
from Database.models import get_db
'''
@author:兰威
'''
class ACmodelHandler:
    @classmethod
    def ac_Model_simply(clas, activity, url):
        '''得到简单活动模型
        :return:  retjson
        '''
        user_headimages = get_db().query(UserImage).filter(UserImage.UIuid == activity.ACsponsorid).all()
        userimg=[]
        for user_headimage in user_headimages:
            exist = get_db().query(Image).filter(Image.IMid == user_headimage.UIimid, Image.IMvalid == 1).all()
            if exist:
                userimg = user_headimage
                break;
        #todo:查找待变更为最新10个
        auth = AuthKeyHandler()
        ac_simply_info = dict(
        ACid=activity.ACid,
        ACtitle=activity.ACtitle,
        ACimgurl=auth.download_url(url),
        ACstartT=activity.ACstartT.strftime('%Y-%m-%d'),
        AClikeN=activity.AClikenumber,
        ACregistN=activity.ACregistN,
        Userimg = auth.download_url(userimg.UIurl)
        )
        return ac_simply_info

