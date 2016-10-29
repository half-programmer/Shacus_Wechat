# -*- coding: utf-8 -*-

'''
微信消息处理
'''
import json

from tornado.template import ParseError
from wechat_sdk.messages import TextMessage, EventMessage

from Wconf import Wconf
from BaseHandlerh import BaseHandler
from wechat_sdk import WechatBasic

class WBasic(BaseHandler):

    conf = Wconf.conf
    wechat = WechatBasic(conf=conf)

    def get(self):
        w_signature = self.get_argument('signature')
        w_timestamp = self.get_argument('timestamp')
        w_nonce = self.get_argument('nonce')
        w_echostr = self.get_argument('echostr')

        wechat = WechatBasic(conf=self.conf)
        if wechat.check_signature(w_signature, w_timestamp, w_nonce):
            print "成功了"
            self.write(json.dumps(int(w_echostr)))
        else:
            print "失败了"

    def post(self):
        body_text  = self.request.body
        try:
            self.wechat.parse_data(body_text)
        except ParseError:
            print 'Invalid Body Text'
        id = self.wechat.message.id  # 对应于 XML 中的 MsgId
        target = self.wechat.message.target  # 对应于 XML 中的 ToUserName
        source = self.wechat.message.source  # 对应于 XML 中的 FromUserName
        time = self.wechat.message.time  # 对应于 XML 中的 CreateTime
        type = self.wechat.message.type  # 对应于 XML 中的 MsgType
        raw = self.wechat.message.raw  # 原始 XML 文本，方便进行其他分析
        print('华丽分割线---------------------------------\n')
        print source
        xml = ''
        if isinstance(self.wechat.message,TextMessage):
            content = self.wechat.message.content
            if content == '活动':
                xml = self.wechat.response_news([
                    {
                        'title': u'第一条新闻标题',
                        'description': u'第一条新闻描述，这条新闻没有预览图',
                        'url': u'http://www.google.com.hk/',
                    }
                ])
        if isinstance(self.wechat.message, EventMessage):
            if self.wechat.message.type == 'click':  # 自定义菜单点击事件
                key = self.wechat.message.key
                if key == 'V1001_BASIC_COURSE':
                    xml = self.wechat.response_news([
                        {
                            'title': u'明天百团，你准备好了吗',
                            'picurl':u'https://mmbiz.qlogo.cn/mmbiz_png/PAKrK0Yx59AVEMlju6Gy6poLNRh9kTgMqqZFibP92rp6W9wl5YMic2lOCcR3RSFn0sOYJXdYb9kBxgOs9VnP3bibQ/0?wx_fmt=png',
                            'url': u'http://mp.weixin.qq.com/s?__biz=MzIxMzUxMDAwMQ==&tempkey=nWACffX4%2B927uhYjH5rqUl9bpsHLCQrxHLHf0HLcu5e7e0I3Zd2WV4pPn9buNfnwMVMudPyeEftXSdFQv1I7XLiZZP%2BxMlt9zW5nbkrIWwfN3GzlaDQTjTGGw8nQr79PFlvb1BfJTMUl%2FMHoXISCSA%3D%3D&#rd',
                        },
                        {
                            'title': u'备受瞩目的摄影棚',
                            'picurl': u'https://mmbiz.qlogo.cn/mmbiz_jpg/PAKrK0Yx59AVEMlju6Gy6poLNRh9kTgMyVMQlIlRicFCyGt6h30zq8kueQeG4NsCXiay1OLDxeTwvgRibNlTaLOmQ/0?wx_fmt=jpeg',
                            'url': u'http://mp.weixin.qq.com/s?__biz=MzIxMzUxMDAwMQ==&tempkey=nWACffX4%2B927uhYjH5rqUl9bpsHLCQrxHLHf0HLcu5eevXEV3KZi9ACKt%2BxkHaiaFsSnmCznlgrHz3VK6EfpcyOBqhMNCNlSP0kTRK2749LN3GzlaDQTjTGGw8nQr79Pxnlb0ghZeR6%2B73YIUHWi9Q%3D%3D&#rd',
                        },
                    ])
                if key == 'V1001_SPECIAL_COURSE':
                    xml = self.wechat.response_news([
                        {
                            'title': u'摄影协会招新啦~',
                            'description': u'我知道一件事',
                            'picurl':u'https://mmbiz.qlogo.cn/mmbiz_jpg/PAKrK0Yx59AggBv2KoFwhBna2IWt3J20bOOYwFWOyuicWSzvZVxJc7G8KPacIQNgzEmd5kdfof6TWzaM0ty53lA/0?wx_fmt=jpeg',
                            'url': u'http://mp.weixin.qq.com/s?__biz=MzIxMzUxMDAwMQ==&tempkey=nWACffX4%2B927uhYjH5rqUl9bpsHLCQrxHLHf0HLcu5e7e0I3Zd2WV4pPn9buNfnwMVMudPyeEftXSdFQv1I7XLiZZP%2BxMlt9zW5nbkrIWwfN3GzlaDQTjTGGw8nQr79PFlvb1BfJTMUl%2FMHoXISCSA%3D%3D&#rd',
                        },
                    ])

        self.write(xml)
