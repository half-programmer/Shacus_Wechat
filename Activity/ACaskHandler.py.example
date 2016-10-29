#-*- coding:utf-8 -*-

'''
@王佳镭
@2016.9.3
'''
import json

from sqlalchemy import desc

import ACFunction
from BaseHandlerh import  BaseHandler
from Database.tables import Image
from Database.tables import User,UserImage
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs

class AskActivity(BaseHandler): #关于用户的一系列活动
    retjson = {'code': '200', 'contents': 'none'}
    def post(self):
        # u_auth_key = self.get_argument('authkey')
        # request_type = self.get_argument('type')
        # u_id = self.get_argument('uid')
        retdata = []  # list array
        type = self.get_argument('type', default='unsolved')
        if type == '10303':  # 1.查看所有活动

                u_id = self.get_argument('uid')
                u_auth_key = self.get_argument('authkey')
                ufuncs = Ufuncs()  # 判断用户权限
                if ufuncs.judge_user_valid(u_id, u_auth_key):  # 用户认证成功
                    try:
                        data=self.db.query(Activity).filter(Activity.ACvalid==1,Activity.ACstatus !=2).order_by(desc(Activity.ACcreateT)).all()
                        length=len(data)
                        print length
                        if length < 10:
                            for i in range(length):

                            #dataimage = self.db.query(ActivityImage).filter(data[i].ACid == ActivityImage.ACLacid).one()
                                datauser=self.db.query(User).filter(data[i].ACsponsorid==User.Uid).one()
                                aclurl = self.db.query(ActivityImage).filter(ActivityImage.ACIacid == data[i].ACid ).limit(1).all()
                                #userurl = self.db.query(UserImage).filter(UserImage.UIuid == datauser.Uid).one()
                                user_headimages = self.db.query(UserImage).filter(
                                    UserImage.UIuid == datauser.Uid).all()
                                userimg = []
                                for user_headimage in user_headimages:
                                    exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                                     Image.IMvalid == 1).all()
                                    if exist:
                                        userimg = user_headimage
                                        break;
                                ACFunction.Acresponse(data[i],datauser,aclurl[0].ACIurl,userimg.UIurl,retdata,u_id)
                                self.retjson['code']='10303'
                                self.retjson['contents']=retdata
                        else:
                            for item in range(0,10):
                             #dataimage = self.db.query(ActivityImage).filter(data[item].ACid == ActivityImage.ACLacid).one()
                             datauser = self.db.query(User).filter(User.Uid == data[item].ACsponsorid).one()
                             aclurl = self.db.query(ActivityImage).filter(ActivityImage.ACIacid == data[item].ACid).limit(1).all()
                             print datauser.Uid
                             print data[item].ACid
                             # userurl = self.db.query(UserImage).filter(UserImage.UIuid == datauser.Uid).one()
                             user_headimages = self.db.query(UserImage).filter(
                                 UserImage.UIuid == datauser.Uid).all()
                             userimg = []
                             for user_headimage in user_headimages:
                                 exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                                     Image.IMvalid == 1).all()
                                 if exist:
                                     userimg = user_headimage
                                     break;
                             ACFunction.Acresponse(data[item],datauser,aclurl[0].ACIurl,userimg.UIurl,retdata,u_id)
                             self.retjson['code'] = '10303'
                             self.retjson['contents'] = retdata
                    except Exception, e:
                        print e
                        self.retjson['code'] = '200'
                        self.retjson['contents'] = 'there is no activity'
                else:
                    self.retjson['code'] = '10373'
                    self.retjson['contents'] = '认证未通过'

        elif type =='10304':    #后来的5个
            u_id = self.get_argument('uid')
            u_auth_key = self.get_argument('authkey')
            ufuncs = Ufuncs()  # 判断用户权限
            if ufuncs.judge_user_valid(u_id, u_auth_key):  # 用户认证成功
                try:
                    acsended=self.get_argument('acsended')
                    Acsended=int(acsended)
                    data=self.db.query(Activity).filter(Activity.ACvalid==1,Activity.ACstatus !=2).order_by(desc(Activity.ACcreateT)).all()
                    length = len(data)
                    print length
                    m_length=length-Acsended
                    print m_length
                    if(m_length==0):
                        self.retjson['code']='10374'
                        self.retjson['contents']='已经没有数据'
                    if (m_length<5):
                        print '小于5个'
                        for i in range(Acsended,length):
                            print i
                            print data[i]
                            #dataimage = self.db.query(ActivityImage).filter(data[i].ACid == ActivityImage.ACLacid).one()
                            datauser = self.db.query(User).filter(User.Uid == data[i].ACsponsorid).one()
                            aclurl = self.db.query(ActivityImage).filter(ActivityImage.ACIacid == data[i].ACid).limit(1).all()
                            #userurl = self.db.query(UserImage).filter(UserImage.UIuid == datauser.Uid).one()
                            user_headimages = self.db.query(UserImage).filter(
                                UserImage.UIuid == datauser.Uid).all()
                            userimg = []
                            for user_headimage in user_headimages:
                                exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                                    Image.IMvalid == 1).all()
                                if exist:
                                    userimg = user_headimage
                                    break;

                            print '哈哈哈'
                            print datauser.Ualais
                            ACFunction.Acresponse(data[i],datauser,aclurl[0].ACIurl,userimg.UIurl,retdata,u_id)
                            print '尼玛还'
                            self.retjson['code'] = '10304'
                            self.retjson['contents'] =retdata
                    else:
                        for item in range(Acsended,acsended+6):
                            #dataimage = self.db.query(ActivityImage).filter(data[item].ACid == ActivityImage.ACLacid).one()
                            datauser = self.db.query(User).filter(data[item].ACsponsorid == User.Uid).one()
                            ACFunction.Acresponse(data[item],datauser,retdata,u_id)
                            self.retjson['code'] = '10304'
                            self.retjson['contents'] = retdata

                except Exception,e:
                    print e
                    self.retjson['code'] = 200
                    self.retjson['contents'] = 'there is no activity'
            else:
                self.retjson['code'] = '10373'
                self.retjson['contents'] = '认证未通过'



        elif type=='10307':#查看活动详情
             data = Activity()
             auth = AuthKeyHandler()
             m_uid=self.get_argument("uid","null")
             auth_key=self.get_argument("authkey","null")
             a_auth = AuthKeyHandler()
             image_urls = []
             ufuncs = Ufuncs() #判断用户权限

             m_ACid=self.get_argument("acid",default="unknown")
             Usermodel = []
             try:
                data=self.db.query(Activity).filter(Activity.ACid==m_ACid).one()
                print '你好'
                print data.ACsponsorid
                acint=data.ACsponsorid
             except Exception,e:
                 print e
             if(data.ACsponsorid == int(m_uid)):
                 issponsor= 1
             else:
                 issponsor= 0




             if ufuncs.judge_user_valid(m_uid,auth_key):  # 用户认证成功
                 try:
                    print '认证成功'
                    data=self.db.query(Activity).filter(m_ACid == Activity.ACid).one() #活动的基本详情
                    #下面是返回用户的信息
                    entryid=self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid==m_ACid,ActivityEntry.ACEregisttvilid == 1).all()
                    for item in entryid:
                        Userjson = {'id': '', 'headImage': ''}
                        Userurls=self.db.query(UserImage).filter(UserImage.UIuid==item.ACEregisterid).all()
                        userimg = []
                        for Userurl in Userurls:
                            exist = self.db.query(Image).filter(Image.IMid == Userurl.UIimid,
                                                                 Image.IMvalid == 1).all()
                            if exist:
                                userimg = Userurl
                                break;
                        Userjson['id'] = item.ACEregisterid
                       # print
                        Userjson['headImage'] = auth.download_url(userimg.UIurl)
                        user = self.db.query(User).filter(User.Uid == item.ACEregisterid).one()
                        Userjson['alais'] = user.Ualais
                        Userjson['sign'] = user.Usign
                        Usermodel.append(Userjson)
                        print Userjson
                        #print Usermodel

                    images = self.db.query(ActivityImage).filter(m_ACid == ActivityImage.ACIacid).all()
                    for image in images:
                       image_url = a_auth.download_url(image.ACIurl)
                       image_urls.append(image_url)

                    ACFunction.response(data,retdata,image_urls,Usermodel,issponsor,m_uid)
                    self.retjson['contents'] = retdata
                    self.retjson['code']='10371'

                 except Exception,e:
                     print e
                     self.retjson['code']='10372'
                     self.retjson['contents']='null information'
             else:
                 self.retjson['code']='10373'
                 self.retjson['contents']='认证未通过'




        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文


