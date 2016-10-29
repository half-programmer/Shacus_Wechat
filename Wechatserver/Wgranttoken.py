# -*- coding: utf-8 -*-
'''
刷新微信access_token
'''

from Wconf import Wconf
conf = Wconf.conf
def GetActoken():

    conf.grant_access_token()
    conf.grant_jsapi_ticket()

GetActoken()