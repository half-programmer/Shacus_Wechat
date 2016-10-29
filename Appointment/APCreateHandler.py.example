# coding=utf-8
'''
  @author:黄鑫晨
  2016.08.29   2016.09.03
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import  User
from FileHandler.ImageHandler import ImageHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs


class APcreateHandler(BaseHandler):  # 创建约拍
    retjson = {'code': '', 'contents': 'None'}

    def post(self):
        # 10201 客户端请求，摄影师发布约拍  start

        ap_type = self.get_argument('type')
        if ap_type == '10201' or ap_type == '10202':  # 请求获得上传权限
            print '进入10201'
            user_phone = self.get_argument('phone')
            auth_key = self.get_argument('auth_key')
            ap_title = self.get_argument('title')
            ap_imgs = self.get_argument('imgs')
            print '获得图片'
            try:
                sponsor = self.db.query(User).filter(User.Utel == user_phone).one()
                print '进入try::::::'
                key = sponsor.Uauthkey
                ap_sponsorid = sponsor.Uid
                print  'ap_sponsorid::::', ap_sponsorid
                print 'ap_title::::', ap_title
                if auth_key == key:  # 认证成功
                    print '认证成功'
                    try:
                        appointment = self.db.query(Appointment).filter(Appointment.APtitle == ap_title).one()
                        if appointment:
                            self.retjson['code'] = '10210'
                            self.retjson['contents'] = r'该约拍已存在'
                    except Exception, e:
                        print e
                        retjson_body = {'auth_key': '', 'apId': ''}
                        auth_key_handler = AuthKeyHandler()
                        ap_imgs_json = json.loads(ap_imgs)
                        retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                        self.retjson['code'] = '10200'
                        if ap_type == '10201':
                            type_ap = 1
                        elif ap_type == '10202':
                            type_ap = 0
                        new_appointment = Appointment(
                            APtitle=ap_title,
                            APsponsorid=sponsor.Uid,
                            APtype=type_ap,
                            APlocation='',
                            APstartT='0000-00-00:00:00:00',
                            APendT='0000-00-00:00:00:00',
                            APcontent='',  # 活动介绍
                            APclosed=0,
                            APlikeN=0,
                            APvalid=0,
                            APaddallowed=0
                        )
                        self.db.merge(new_appointment)
                        self.db.commit()
                        try:
                            print '插入成功，进入查询'
                            ap = self.db.query(Appointment).filter(
                                   Appointment.APtitle == ap_title, Appointment.APsponsorid == ap_sponsorid).one()
                            ap_id = ap.APid
                            retjson_body['apId'] = ap_id

                            self.retjson['contents'] = retjson_body
                        except Exception, e:
                            print '插入失败！！'
                            self.retjson['contents'] = r'服务器插入失败'
                else:
                    self.retjson['code'] = '10211'
                    self.retjson['contents'] = r'用户授权码错误'
            except Exception, e:
                print e
                self.retjson['code'] = '10212'
                self.retjson['contents'] = "该用户名不存在"
        elif ap_type == '10205':  # 开始传输数据
            print "进入10205"
            # todo ：如果完成约拍发起第一步没有完成第二步，在返回时应该过滤掉这些活动
            ap_id = self.get_argument('apid')
            auth_key = self.get_argument('auth_key')
            # todo: auth_key经常使用，可以优化
            ap_title = self.get_argument('title')
            ap_start_time = self.get_argument('start_time')
            ap_end_time = self.get_argument('end_time')
            ap_join_time = self.get_argument('join_time')
            ap_location = self.get_argument('location')
            ap_free = self.get_argument('free')
            ap_price = self.get_argument('price')
            ap_content = self.get_argument('contents')
            ap_tag = self.get_argument('tags')  # 约拍标签？确认长度
            ap_addallowed = self.get_argument('ap_allowed')
            ap_type = self.get_argument('ap_type')
            ap_imgs = self.get_argument('imgs')
            try:
                ap_imgs_json = json.loads(ap_imgs)
                user = self.db.query(User.Uid).filter(User.Uauthkey == auth_key).one()  # 查看该用户id
                uid = user.Uid
                print 'uid: ', uid
                print '找到用户id'
                try:
                    print '判断该活动是否已经存在'
                    exist = self.db.query(Appointment).filter(Appointment.APtype == ap_type,
                                                              Appointment.APtitle == ap_title,
                                                              Appointment.APsponsorid == uid,
                                                              Appointment.APcontent == ap_content
                                                              ).one()  # 判断该活动是否已经存在
                    if exist:
                        print '活动存在'
                        self.retjson['code'] = '10210'
                        self.retjson['contents'] = '该约拍已存在'
                except Exception, e:
                    print e
                    try:
                        exist = self.db.query(Appointment).filter(Appointment.APid == ap_id,
                                                                  Appointment.APtitle == ap_title
                                                                  ).one()
                        print '判断授权是否存在'
                        if exist:
                            ap_sponsorid = exist.APsponsorid
                            if uid == ap_sponsorid:
                                print '授权存在'
                                self.db.query(Appointment).filter(Appointment.APid == ap_id). \
                                    update({Appointment.APstartT: ap_start_time, Appointment.APendT: ap_end_time,
                                            Appointment.APjoinT: ap_join_time,
                                            Appointment.APlocation: ap_location, Appointment.APfree: ap_free,
                                            Appointment.APcontent: ap_content,
                                            Appointment.APaddallowed: ap_addallowed,
                                            Appointment.APtype: ap_type,
                                            Appointment.APvalid: 1
                                            }, synchronize_session=False)
                                imghandler = ImageHandler()
                                try:
                                    imghandler.insert_appointment_image(ap_imgs_json, ap_id)
                                except Exception, e:
                                    print e, '网络故障'
                                    self.retjson['contents'] = u'网络故障'
                                self.db.commit()
                                self.retjson['code'] = '10214'
                                self.retjson['contents'] = '发布约拍成功'
                            else:
                                print 'fd'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '10213'
                        self.retjson['contents'] = r'该发布尚未获得权限！'
            except Exception, e:
                print e
                self.retjson['code'] = '10211'
                self.retjson['contents'] = r'用户授权码错误！'

        # 取消约拍
        elif ap_type == '10207':
            auth_key = self.get_argument('authkey')
            apid = self.get_argument('apid')
            uid = self.get_argument('userid')
            ufunc = Ufuncs()
            if ufunc.judge_user_valid(uid, auth_key):
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == apid).one()
                    if appointment.APvalid == 1:
                        # 约拍还有效
                        if appointment.APsponsorid == int(uid):
                            # 报名中，可以取消
                            if appointment.APstatus == 0:
                                appointment.APvalid = 0
                                self.db.commit()
                                self.retjson['code'] = '10200'
                                self.retjson['contents'] = '成功取消约拍！'
                            else:
                                self.retjson['code'] = '10215'
                                self.retjson['contents'] = '该约拍正在进行中或已完成，不能取消！'
                        else:
                            self.retjson['code'] = '10216'
                            self.retjson['contents'] = '该用户不是发起人，无权利取消'
                    else:
                        self.retjson['code'] = '10217'
                        self.retjson['contents'] = '该约拍之前已被取消！'
                except Exception ,e:
                    self.retjson['code'] = '10218'
                    self.retjson['contents'] = '该约拍不存在！'
            else:
                self.retjson['code'] = '10211'
                self.retjson['contents'] = '用户授权错误'
        else:
            print 'ap_type: ', ap_type
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

        # 判断返回是否许可

        # 10201 客户端请求，摄影师发布约拍 end






