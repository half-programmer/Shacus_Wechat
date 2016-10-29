# -*- coding: utf-8 -*-
'''
微信创建菜单
'''
from wechat_sdk.exceptions import OfficialAPIError

from BaseHandlerh import BaseHandler
from Wconf import Wconf
from wechat_sdk import WechatBasic


def createmenu():
    '''
    创建微信菜单
    Returns:

    '''
    conf = Wconf.conf
    wechat = WechatBasic(conf=conf)
    # menu = {
    #         'button':[
    #             {
    #                 'name':'教程',
    #                 'sub_button':[
    #                     {
    #                         'type':'click',
    #                         'name':'基础教程',
    #                         'key':'V1001_BASIC_COURSE'
    #                     },
    #                     {
    #                         'type': 'click',
    #                         'name': '专题教程',
    #                         'key': 'V1001_SPECIAL_COURSE'
    #                     }
    #                 ]
    #             },
    #             {
    #                 'name':'约拍',
    #                 'sub_button':[
    #                     {
    #                         'type':'view',
    #                         'name':'摄影师单',
    #                         'url':'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '模特单',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '我要发单',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '约拍伴侣',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '我的约拍',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                 ]
    #             },
    #             {
    #                 'name':'活动',
    #                 'sub_button':[
    #                     {
    #                         'type':'view',
    #                         'name':'往期活动',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '活动预告及报名',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                     {
    #                         'type': 'view',
    #                         'name': '发起活动',
    #                         'url': 'http://www.soso.com/'
    #                     },
    #                 ]
    #             },
    #         ]
    #     }
    menu ={
            'button':[
                {
                    'name':'活动',
                    'sub_button':[
                        {
                            'type':'click',
                            'name':'历史活动',
                            'key':'V1001_BASIC_COURSE'
                        },
                        {
                            'type': 'click',
                            'name': '活动预告',
                            'key': 'V1001_SPECIAL_COURSE'
                        }
                    ]
                },
        ]
    }
    try:
        wechat.create_menu(menu)
    except OfficialAPIError,e:
        print e

createmenu()