# -*- coding: utf-8 -*-
import time

from Database.models import get_db
from Database.tables import UserImage,Image, WApImage, WAcImage, WDImage, WApCompanionImage

'''
 创建者：兰威 黄鑫晨
 创建时间：2016-08-30 18:05
'''
class ImageHandler(object):
    #def __init__(self):

    def change_wap_image(self, img_urls, wap_id):

            db = get_db()
            for img_url in img_urls:
                # 如果原来有这张图
                try:
                    wap_img = db.query(WApImage).filter(WApImage.WAPIurl == img_url).one()
                    wap_img.WAPIvalid = 1
                # 如果原来没有
                except Exception, e:
                    print 'fdfdf' + e
                    newimg = []
                    newimg.append(img_url)
                    imids = self.insert_wappointment_image(newimg, wap_id)
            try:
                db.commit()
            except Exception, e:
                print e

    # @staticmethod
    def insert_wappointment_image(self, list, wap_id):
        '''
        Args:
            list: 图片名字的数组
            ap_id: 微信约拍的ID
        Returns:
        '''
        # 先过滤

        imids = self.insert(list)
        for i in range(len(imids)):
            image = WApImage(
                WAPIapid=wap_id,
                WAPIimid=imids[i],
                WAPIurl=list[i]
            )
            db = get_db()
            db.merge(image)
            db.commit()

    def delete_wappointment_image(self, ap_id):
        '''
        Args:
            list: 图片名字的数组
            ap_id: 微信约拍的ID
        Returns:
        '''
        db = get_db()
        try:
            ap_imgs = db.query(WApImage).filter(WApImage.WAPIapid == ap_id).all()
            for ap_img in ap_imgs:
                ap_img.WAPIvalid = 0
            db.commit()
        except Exception, e:
            print e

    # @staticmethod
    def insert(self,list):
        '''
        向数据库插入图片链接
        :param list: 图片名的列表
        :table: 应该插入的表名
        :return:
        '''
        db = get_db()
        new_imids=[]
        imid = ''
        for img_name in list:  # 第一步，向Image里表里插入
            image = Image(
                    IMvalid=1,
                    IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                    IMname=img_name
                )
            db.merge(image)
            db.commit()
            new_imgs = db.query(Image).filter(Image.IMname == img_name).all()
            for new_img in new_imgs:
                imid = new_img.IMid
            new_imids.append(imid)
        return new_imids

    # @staticmethod
    def insert_wdynamic_image(self, list, wdy_id):
        '''
        Args:
            list: 图片名字的数组
            ap_id: 微信约拍的ID
        Returns:
        '''
        # 先过滤

        imids = self.insert(list)
        for i in range(len(imids)):
            image = WDImage(
                WDIwdid=wdy_id,
                WDIimid=imids[i],
                WDIurl=list[i]
            )
            db = get_db()
            db.merge(image)
            db.commit()
    def insert_user_image(self, list, uid):
        # type: (object, object) -> object
        '''

        Args:
            list:图片名字的数组
            uid: 用户的ID

        Returns:

        '''

        imids = self.insert(list)
        for i in range(len(imids)):
            image = UserImage(
                UIuid=uid,
                UIimid=imids[i],
                UIurl=list[i]
            )
            db = get_db()
            db.merge(image)
            db.commit()

    # @staticmethod
    def insert_activity_image(self,list,ac_id):
        '''

        Args:
            list: 图片的名字的数组
            ac_id: 活动的ID

        Returns:

        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = WAcImage(
                WACIacid=ac_id,
                WACIimid=imids[i],
                WACIurl=list[i]
            )
            db = get_db()
            db.merge(image)
            db.commit()

    # @staticmethod

    def insert_appointment_image(self,list,ap_id):
        '''

        Args:
            list: 图片名字的数组
            ap_id: 约拍的ID


        Returns:

        '''
        imids = self.insert(list)
        for i in range(len(imids)):
            image = WAcImage(
                APIapid=ap_id,
                APIimid=imids[i],
                APIurl=list[i]
            )
            db = get_db()
            db.merge(image)
            db.commit()


    def change_user_headimage(self,newimage,uid):
        db = get_db()
        images = db.query(UserImage).filter(UserImage.UIuid == uid,UserImage.UIvalid == 1).all()
        for image in images:
            image.UIvalid = 0
            image_id = image.UIimid
            im = db.query(Image).filter(Image.IMid == image_id).one()
            if im.IMvalid == 1:
                im.IMvalid = 0
        db.commit()
        self.insert_user_image(newimage,uid)

    def insert_appointment_image(self, list, ap_id):
            '''

            Args:
                list: 图片名字的数组
                ap_id: 约拍的ID


            Returns:

            '''
            imids = self.insert(list)
            for i in range(len(imids)):
                image = WAcImage(
                    APIapid=ap_id,
                    APIimid=imids[i],
                    APIurl=list[i]
                )
                db = get_db()
                db.merge(image)
                db.commit()

    def insert_companion_image(self, list, Companion_id):  # 插入约拍伴侣图片
                    '''

                    Args:
                        list: 图片的名字的数组
                        ac_id: 约拍伴侣的id

                    Returns:

                    '''
                    imagehandler = ImageHandler()
                    imids = imagehandler.insert(list)
                    for i in range(len(imids)):
                        image = WApCompanionImage(
                            WAPCid=Companion_id,
                            WAPCimid=imids[i],
                            WAPCurl=list[i],
                            WAPCvalid=1
                        )
                        db = get_db()
                        db.merge(image)
                        db.commit()







                     #print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# timen = time.strftime('%Y-%m-%dT%H:%M:%S')
# timeStamp = int(time.mktime(timen))
# print timeStamp