# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍模型
@datatime：2016.10.10
r :兰威
@type：微信的约拍模型
@datatime：2016.10.10
'''
from Database.models import get_db
from Database.tables import User, WApImage, WApFinish, UserImage, WApCompanionImage
from FileHandler.Upload import AuthKeyHandler

class WAPmodel(object):

    def wap_model_simply_one(self, wap, picurl):
        '''

        Args:
            wap: 约拍的一个实例
            picurl: 约拍图片的地址（第一张）

        Returns: wap简单模型

        '''
        db = get_db()
        try:
            status_item = wap.WAPstatus
            if(status_item == 3):
                status_item = 2
            user = db.query(User).filter(User.Uid == wap.WAPsponsorid).one()
            u_alias = user.Ualais
            u_sex = user.Usex
            headimg = db.query(UserImage).filter(UserImage.UIuid == wap.WAPsponsorid,UserImage.UIvalid == 1).one()
            auth = AuthKeyHandler()
            ret_ap = dict(
                title=wap.WAPtitle,
                content=wap.WAPcontent[0:12],
                picurl=auth.download_abb_url(picurl),
                id=wap.WAPid,
                #detailurl='www.baidu.com'  #当前传的是一个假的值
                #sponsorid=wap.WAPsponsorid,
                alais=u_alias,
                sex=int(u_sex),
                type=int(wap.WAPtype),
                status = status_item,
                registn = wap.WAPregistN,
                headimg=auth.download_abb_url(headimg.UIurl)
            )
            return ret_ap
        except Exception, e:
            print e


    def wap_model_simply_more(self,waps,picurls):
        '''

        Args:
            waps: 约拍实例的元组
            picurls: 约拍图片地址的元组

        Returns:

        '''
        retedate = []
        for wap,picurl in zip(waps,picurls):
            data = self.wap_model_simply_one(wap,picurl)
            retedate.append(data)
        return retedate


    def wap_model_mutiple(self,wap,picurls,issp,isre,isco,userlist,m_id):
        '''

        Args:
            wap: 约拍实例
            picurls: 约拍的图片组
            issp:是否是发布者
            isre:是否报名
            isco:是否被选择

        Returns:

        '''
        db = get_db()
        status_item = wap.WAPstatus
        if(status_item == 3):
            finishmen = db.query(WApFinish).filter(WApFinish.WAFapid == wap.WAPid,WApFinish.WAFuid == m_id).all()
            if finishmen:
                status_item = 3
            else :
                status_item = 2

        user = db.query(User).filter(User.Uid == wap.WAPsponsorid).one()
        u_alias = user.Ualais
        u_sex = user.Usex
        auth = AuthKeyHandler()
        picture_data = []
        headimg = db.query(UserImage).filter(UserImage.UIuid == wap.WAPsponsorid, UserImage.UIvalid == 1).one()
        for pic in picurls:
            picture_data.append(auth.download_url(pic))
        ret_ap = dict(
            title=wap.WAPtitle,
            content=wap.WAPcontent,
            picurl=picture_data,
            id=wap.WAPid,
            alias=u_alias,
            # detailurl='www.baidu.com'  #当前传的是一个假的值
            sponsorid=wap.WAPsponsorid,
            sex=int(u_sex),
            location=wap.WAPlocation,
            free=int(wap.WAPfree),
            time=wap.WAPtime,
            type=int(wap.WAPtype),
            registn=wap.WAPregistN,
            status=status_item,
            issponsorid=issp,
            isregist=isre,
            ischoosed=isco,
            user=userlist,
            headimg=auth.download_abb_url(headimg.UIurl)
        )
        return ret_ap

    def wap_model_getchangeinfo(self, wap):
        '''

        Args:
            wap:约拍实例

        Returns:

        '''
        db = get_db()
        pics = db.query(WApImage).filter(WApImage.WAPIapid == wap.WAPid, WApImage.WAPIvalid == 1).all()

        auth = AuthKeyHandler()
        picurls = []
        keys = []
        for pic in pics:
            picurls.append(auth.download_url(pic.WAPIurl))
            keys.append(pic.WAPIurl)
        ret_ap = dict(
            contents=wap.WAPcontent,
            picurl=picurls,
            key=keys,
        )
        return ret_ap

    def ApCompanion(clas, Companion, retdata):
        auth = AuthKeyHandler()
        Companion_imgs = get_db().query(WApCompanionImage).filter(WApCompanionImage.WAPCid == Companion.WAPCid).all()
        Imgs = []
        for item in Companion_imgs:
            Imgs.append(auth.download_url(item.WAPCurl))
        ApCompanion_model = dict(
            CompanionId=Companion.WAPCid,
            CompanionTitle=Companion.WAPCname,
            CompanionContent=Companion.WAPCServeintro,
            CompanionUrl=Companion.WAPCContact,
            CompanionPic=Imgs,
        )
        retdata.append(ApCompanion_model)



