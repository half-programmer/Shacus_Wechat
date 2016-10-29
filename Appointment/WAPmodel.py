# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的约拍模型
@datatime：2016.10.10
'''
from Database.models import get_db
from Database.tables import User
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
        user = db.query(User).filter(User.Uid == wap.WAPsponsorid).one()
        u_alias = user.Ualais
        u_sex = user.Usex
        auth = AuthKeyHandler()
        ret_ap = dict(
            title=wap.WAPtitle,
            content=wap.WAPcontent[0:12],
            picurl=auth.download_url(picurl),
            id=wap.WAPid,
            #detailurl='www.baidu.com'  #当前传的是一个假的值
            #sponsorid=wap.WAPsponsorid,
            alais=u_alias,
            sex=int(u_sex),
            type=int(wap.WAPtype),
            status = wap.WAPstatus,
            registn = wap.WAPregistN,
        )
        return ret_ap

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


    def wap_model_mutiple(self,wap,picurls,issp,isre,isco,userlist):
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
        user = db.query(User).filter(User.Uid == wap.WAPsponsorid).one()
        u_alias = user.Ualais
        u_sex = user.Usex
        auth = AuthKeyHandler()
        picture_data = []
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
            status=wap.WAPstatus,
            issponsorid=issp,
            isregist=isre,
            ischoosed=isco,
            user=userlist,
        )
        return ret_ap

