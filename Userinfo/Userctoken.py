# coding=utf-8
'''
@author :兰威
@type ： 用于获得用户聊天时的token
'''

from rongcloud import RongCloud

def get_token(uid,nickname):
    rcloud = RongCloud("x4vkb1qpvxu4k", "EziWuNBddbcfz")
    c = rcloud.User.getToken(userId=uid, name=nickname,portraitUri='').result
    return c['token']





