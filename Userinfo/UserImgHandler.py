#-*- coding:utf-8 -*-
'''
author:wjl
2016.10.26
'''
import time

from BaseHandlerh import BaseHandler
from Database.models import get_db
from Database.tables import Image, Homepageimage, User


class UserImgHandler(object):
    def delete_Homepage_image(self,utel):#先注释掉该用户的所有图片

        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Utel == utel).one()
            allimage=  db.query(Homepageimage).filter(Homepageimage.HPuser == userinfo.Uid).all()
            for item in allimage:
                item.HPimgvalid = 0
            db.commit()

        except Exception ,e:
            print e
            print 'the user doesn\'t exsit'
    def change_Homepage_image(self,list,utel):#改变图片信息
        try:
            db=get_db()
            usertel = db.query(User).filter(User.Utel == utel).one()
            for item in list:#如果有那么重置为1，如果没有就继续保持0
                try:
                    userimage = db.query(Homepageimage).filter(Homepageimage.HPuser == usertel.Uid , Homepageimage.HPimgurl == item).one()
                    userimage.HPimgvalid = 1
                    db.commit()



                except Exception ,e:#新的需要插入
                    print 'insert new Homepageimage'
                    itemlist = []
                    itemlist.append(item)
                    self.insert_Homepage_image(itemlist,utel)
        except Exception,e:
            print e
            print 'doesn\'t exsit'



    def insert_Homepage_image(self,list,utel):

        try:
            db = get_db()
            usertel = db.query(User).filter(User.Utel == utel).one()
            HPimg = self.insert(list)

            for i in range(len(HPimg)):
                new_hpimg= Homepageimage(

                HPuser = usertel.Uid,
                HPUimage = HPimg[i],
                HPimgurl = list[i],
                HPimgvalid = True,
                )
                db.merge(new_hpimg)
                db.commit()
        except Exception, e:
            print e

    def insert(self,list):
            db=get_db()
            new_imids = []

            for img_name in list:  # 第一步，向Image里表里插入
                image = Image(
                    IMvalid = True,
                    IMT = time.strftime('%Y-%m-%d %H:%M:%S'),
                    IMname = img_name,
                )

                db.merge(image)
                db.commit()
                try:
                    new_img = get_db().query(Image).filter(Image.IMname == img_name).one()
                    imid = new_img.IMid
                    new_imids.append(imid)
                except Exception, e:
                    print e
            return new_imids