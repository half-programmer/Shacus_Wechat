# -*- coding: utf-8 -*-

'''
@type:微信基本配置
@author:兰威
@datatime : 2016.10.1
'''

import sys
sys.path.append("..")
from wechat_sdk import WechatConf
from BaseHandlerh import BaseHandler
from Database.tables import WeAcToken
from Database.models import get_db
class Wconf(BaseHandler):

    def get_access_token_function():
        '''
        获取access_token
        :return: 注意返回值为一个 Tuple，第一个元素为 access_token 的值，第二个元素为 access_token_expires_at 的值
        '''
        db = get_db()
        data = db.query(WeAcToken).all()
        token = (data[0].WACtoken, data[0].WACexpire)
        return token

    def set_access_token_function(access_token, access_token_expires_at):
        db = get_db()
        weactoken = db.query(WeAcToken).all()
        if weactoken == []:
            actoken = WeAcToken(
                WACexpire=access_token_expires_at,
                WACtoken=access_token,
            )
            db.merge(actoken)
        else:
            weactoken[0].WACexpire = access_token_expires_at
            weactoken[0].WACtoken = access_token
        try:
            db.commit()
        except Exception, e:
            print e
            db.roolback()

    def get_jsapi_ticket_function():

        """
        获取jsapi_ticket
        注意返回值为一个 Tuple，第一个元素为 jsapi_ticket 的值，第二个元素为 jsapi_ticket_expires_at 的值
        """
        db = get_db()
        data = db.query(WeAcToken).all()
        token = (data[1].WACtoken, data[1].WACexpire)
        return token

    def set_jsapi_ticket_function(jsapi_ticket, jsapi_ticket_expires_at):
        '''
        设置jsapi_ticket和jsapi_ticket_expires_at
        Args:
            jsapi_ticket
            jsapi_ticket_expires_at


        Returns:

        '''
        db = get_db()
        weactoken = db.query(WeAcToken).all()
        if len(weactoken) == 1:
            actoken = WeAcToken(
                WACexpire=jsapi_ticket_expires_at,
                WACtoken=jsapi_ticket,
            )
            db.merge(actoken)
        else:
            weactoken[1].WACexpire = jsapi_ticket_expires_at
            weactoken[1].WACtoken = jsapi_ticket
        try:
            db.commit()
        except Exception, e:
            print e
            db.roolback()

    conf = WechatConf(
        token='xtIRzP0tcQuGqcgWiu',
        appid='wx0c9dd1c77d3e5295',#测试的id：wx679493e73b1bd83b,真实id:wx0c9dd1c77d3e5295
        appsecret='ed3eee4636d9ab4068c7eb5ca14ddb59',#测试秘钥;f1dad656a7269b068834b5007991b46b，真实秘钥：ed3eee4636d9ab4068c7eb5ca14ddb59
        encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
        #encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
        access_token_getfunc=get_access_token_function,
        access_token_setfunc=set_access_token_function,
        jsapi_ticket_getfunc=get_jsapi_ticket_function,
        jsapi_ticket_setfunc=set_jsapi_ticket_function,

    )


