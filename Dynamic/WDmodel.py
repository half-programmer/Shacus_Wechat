# -*-coding:utf-8 -*-
'''
@author :兰威
@type：微信的动态模型
@datatime：2016.11.22
'''
from Database.tables import UserImage, User
from Database.models import get_db
from FileHandler.Upload import AuthKeyHandler


class WDmodel(object):

    def wd_model_simply_one(self,wd,picurl):
        '''
        动态的一个简单model
        Args:
            wd: 动态的一个实例
            picurl: 动态的图片地址（第一张）

        Returns:wd简单模型

        '''
        db = get_db()
        try:
            u_id = wd.WDsponsorid
            u_himg = db.query(UserImage).filter(UserImage.UIuid == u_id,UserImage.UIvalid == 1).one()
            himg_url = u_himg.UIurl
            auth = AuthKeyHandler()
            ret_ap = dict(
                contents=wd.WDcontents,
                headimg=auth.download_abb_url(himg_url),
                uid=u_id,
                # detailurl='www.baidu.com'  #当前传的是一个假的值
                # sponsorid=wap.WAPsponsorid,
                did=wd.WDid,
                dimg=auth.download_url(picurl),
            )
            return ret_ap
        except Exception,e:
            print e

    def wd_model_simply_more(self, wds, picurls):
        '''

        Args:
            wds: 动态实例数组
            picurls: 图片数组

        Returns:

        '''
        retedate = []
        for wap,picurl in zip(wds,picurls):
            data = self.wd_model_simply_one(wap,picurl)
            retedate.append(data)
        return retedate

    def wd_model_multiply_one(self, wd, picurls):
        '''
        动态的一个简单model
        Args:
            wd: 动态的一个实例
            picurl: 动态的图片地址（第一张）

        Returns:wd简单模型

        '''
        db = get_db()
        try:
            u_id = wd.WDsponsorid
            u_himg = db.query(UserImage).filter(UserImage.UIuid == u_id, UserImage.UIvalid == 1).one()
            himg_url = u_himg.UIurl
            auth = AuthKeyHandler()
            pic_urls = []
            user = db.query(User).filter(User.Uid == u_id,User.Uvalid == 1).one()
            u_alias = user.Ualais
            for picurl in picurls:
                pic_urls.append(auth.download_url(picurl.WDIurl))
            ret_ap = dict(
                contents=wd.WDcontents,
                headimg=auth.download_abb_url(himg_url),
                uid=u_id,
                # detailurl='www.baidu.com'  #当前传的是一个假的值
                # sponsorid=wap.WAPsponsorid,
                alias = u_alias,
                did=wd.WDid,
                dimgs=pic_urls,
            )
            return ret_ap
        except Exception, e:
            print e