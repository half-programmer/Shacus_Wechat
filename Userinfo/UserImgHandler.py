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
            new_imids = []
            for img_name in list:  # 第一步，向Image里表里插入
                image = Image(
                    IMvalid = True,
                    IMT = time.strftime('%Y-%m-%d %H:%M:%S'),
                    IMname = img_name,
                )
                db = get_db()
                db.merge(image)
                db.commit()
                try:
                    new_img = get_db().query(Image).filter(Image.IMname == img_name).one()
                    imid = new_img.IMid
                    new_imids.append(imid)
                except Exception, e:
                    print e
            return new_imids