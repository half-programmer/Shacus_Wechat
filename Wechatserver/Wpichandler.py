# -*- coding: utf-8 -*-
'''
@author:兰威
@datatime：2016。10.08
@type:微信图片处理，包含从微信服务器下载和图片的上传至七牛云图片
'''
import json
import sys
sys.path.append("..")
from BaseHandlerh import BaseHandler
from Wconf import Wconf
from wechat_sdk import WechatBasic
from FileHandler.Upload import AuthKeyHandler
from qiniu import Auth
from qiniu.services.storage.uploader import put_file
import os
import sys

class Wpichandler(BaseHandler):


    conf = ''
    wechat = ''

    def __init__(self):
        self.conf = Wconf.conf
        self.wechat = WechatBasic(conf=self.conf)

    def getfromwechat(self,media_ids,names):
        '''

        Args:
            media_ids: 图片的media_id数组
            names: 图片的名字数组

        Returns: null

        '''
        #media_ids = json.loads(media_ids)
        #names = json.loads(names)
        for media_id, name in zip(media_ids, names):
            response = self.wechat.download_media(media_id=media_id)
            with open('./{address}'.format(address=name), 'wb') as fd:
                for chunk in response.iter_content(1024):
                    fd.write(chunk)

    def upload(self,names):
        '''

        Args:
            names:图片的media数组

        Returns:所有图片上传成功时，返回True，否则为False

        '''
        auth = AuthKeyHandler()
        #names = json.loads(names)
        bucket_name = 'shacus'
        q = Auth(auth.access_key,auth.secret_key)
        for name in names:
            token = q.upload_token(bucket_name,name,345600)
            localfile = './{address}'.format(address=name)
            ret,info = put_file(token,name,localfile)
            if  info.status_code != 200:
                return False
        return True

    def pichandler(self,media_ids,names):
        '''

        Args:
             media_ids: 图片的media_id数组
            names: 图片的名字数组

        Returns:所有图片上传成功时，返回True，否则为False

        '''

        self.getfromwechat(media_ids=media_ids,names=names)
        if self.upload(names=names):
            #names = json.loads(names)
            for name in names:
                filename = '{mulu}/{address}'.format(address=name,mulu=sys.path[0])
                if os.path.exists(filename):
                    os.remove(filename)
            return True




