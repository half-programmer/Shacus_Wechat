# -* coding:utf-8 *-
'''
@author:黄鑫晨
@time：2016-10-24
@introduce：返回用户个人信息
'''
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, WApInfo, WAppointment, Homepageimage
from FileHandler.Upload import AuthKeyHandler


class UHandler(BaseHandler):
    retjson = {'code': '200', 'sign': '', 'comments': '', 'imgs': '', 'contents': '', 'alais': '', 'sex': ''}

    def get_comment(self, uid):
        '''
        获得用户的评论(被评)
        Args:
            uid: 用户Id

        Returns:评论列表

        '''

        comments = []
        try:
            # 用户作为摄影师参加的约拍
            asphotoers = self.db.query(WApInfo).filter(WApInfo.WAIpid == uid).all()
            for each in asphotoers:
                first = asphotoers[0]  # 如果是空直接抛出异常
                # 模特对摄影师的评论
                if each.WAImcomment:
                    comment_content = each.WAImcomment
                    score = each.WAIpscore  # 摄影师获得的评分
                    comment_user_id = each.WAImid  # 模特的id
                    mcommentT = each.WAImcommentT   # 模特对摄影师的评论的时间
                    apid = each.WAIappoid

                    try:
                        model = self.db.query(User).filter(User.Uid == comment_user_id).one()
                        appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == apid).one()
                        ap_name = appointment.WAPtitle
                        model_name = model.Ualais
                        comment_entry = dict(
                                comment=comment_content,
                                alais=model_name,
                                score=score,
                                title=ap_name,
                                time=mcommentT.strftime('%Y-%m-%d')

                        )
                        comments.append(comment_entry)
                        self.retjson['code'] = '200'
                        self.retjson['contents'] = u"成功"
                    except Exception, e:
                        self.retjson['code'] = u'40005'
                        self.retjson['contents'] = u"获取评论用户出错"
        except Exception, e:
            print e
            self.retjson['code'] = u'40002'
            self.retjson['contents'] = u"该用户作为摄影师没有发布过约拍"
        try:
            # 用户作为模特参加的约拍
            asmodels = self.db.query(WApInfo).filter(WApInfo.WAImid == uid).all()
            first = asmodels[0]  # 如果是空直接抛出异常
            for each in asmodels:
                # 摄影师对模特的评论:
                if each.WAIpcomment:
                    comment_content = each.WAIpcomment
                    comment_user_id = each.WAIpid  # 摄影师的id
                    score = each.WAImscore  # 模特获得的评分
                    pcommentT = each.WAIpcommentT  # 摄影师对模特的评论的时间

                    apid = each.WAIappoid
                    try:
                        photoer = self.db.query(User).filter(User.Uid == comment_user_id).one()
                        appointment = self.db.query(WAppointment).filter(WAppointment.WAPid == apid).one()
                        photoer_name = photoer.Ualais

                        ap_name = appointment.WAPtitle
                        comment_entry = dict(
                            comment=comment_content,
                            alais=photoer_name,
                            score=score,
                            title=ap_name,
                            time=pcommentT.strftime('%Y-%m-%d')
                        )
                        comments.append(comment_entry)
                        self.retjson['code'] = '200'
                        self.retjson['contents'] = u"成功"
                    except Exception, e:
                        self.retjson['code'] = '40005'
                        self.retjson['contents'] = u"获取评论用户出错"
        except Exception, e:
            print e
            self.retjson['code'] = u'40003'
            self.retjson['contents'] = u"该用户作为模特没有发布过约拍"
        if comments:
            self.retjson['code'] = u'200'
            self.retjson['comments'] = comments
            self.retjson['contents'] = u"获取个人主页成功"
        else:
            self.retjson['code'] = u'20002'
            self.retjson['contents'] = u"他还没有评论哦，来做第一个沙发"

    def get(self):
        self.retjson = {'code': '200', 'sign': '', 'comments': '', 'imgs': '', 'contents': '', 'alais': '', 'sex': ''}
        type = self.get_argument('type')
        callback = self.get_argument("jsoncallback")
        # 请求用户自己的个人主页
        if type == '1':
            # openid = self.get_argument('openid')
            utel = self.get_argument('utel')
            try:
                #user = self.db.query(User).filter(User.Uopenid == openid).one()
                user = self.db.query(User).filter(User.Utel == utel).one()
                u_alais = user.Ualais  # 用户自己的昵称
                usex = user.Usex
                uid = user.Uid
                sign = user.Usign
                if u_alais:
                    self.retjson['alais'] = u_alais  # 昵称
                if sign:
                    self.retjson['sign'] = sign
                if usex:
                    self.retjson['sex'] = int(usex)
                self.get_comment(uid)

            except Exception, e:
                print e
                self.retjson['code'] = u'40001'
                self.retjson['contents'] = u"该用户不存在"

        # 看别人的个人主页
        elif type == '2':
            utel = self.get_argument('utel')  # 发起请求的用户的加密后的手机号
            uid_other = self.get_argument('uid')  # 被看个人主页的用户的Id
            try:
                user = self.db.query(User).filter(User.Utel == utel).one()
                if user:
                    try:
                        user_other = self.db.query(User).filter(User.Uid == uid_other).one()
                        u_alais_other = user_other.Ualais
                        usex = user_other.Usex
                        if usex:
                            self.retjson['sex'] = int(usex)
                        if u_alais_other:
                            self.retjson['alais'] = u_alais_other
                        self.get_comment(uid_other)
                        auth_key_handler = AuthKeyHandler()
                        img_tokens = []
                        try:
                            u_homepage_imgs = self.db.query(Homepageimage).filter(Homepageimage.HPuser == uid_other).all()
                            for each in u_homepage_imgs:
                                img_url = each.HPimgurl
                                img_tokens.append(auth_key_handler.download_url(img_url))
                        except Exception, e:
                            img_tokens = ''
                        self.retjson['imgs'] = img_tokens
                    except Exception, e:
                        print e
                        self.retjson['code'] = u'40004'
                        self.retjson['contents'] = u"被看用户不存在"
            except Exception, e:
                print e
                self.retjson['code'] = u'40001'
                self.retjson['contents'] = u"请求用户不存在"
        jsonp = "{jsfunc}({json});".format(jsfunc=callback, json=json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.write(jsonp)




