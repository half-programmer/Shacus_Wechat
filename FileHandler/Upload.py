# -*- coding: utf-8 -*-
# flake8: noqa
'''
 作用：处理七牛云上传凭证获取
 创建者：兰威
 创建时间：2016-08-30 18:05
'''
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

# todo 封装auth_token
class AuthKeyHandler:
    def __init__(self):
        self.access_key = 'yzAza_Cm87nXkh9IyFfpg7LL7qKJ097VK5IOpLj0'
        self.secret_key = 'GFWHU9hYkU4hepDwpWfHaNDt3gJCDsAk3Kz6DGdk'
        self.Auth_key = Auth(self.access_key, self.secret_key)
        self.auth_tokens = []
    # 构建鉴权对象
    def generateToken(self,names):
       bucket_name = 'shacus' # 要上传的空间
       tokens = []
       for title in names:
           print 'title:',title
           token = self.Auth_key.upload_token(bucket_name, title, 345600)
           self.auth_tokens.append(token)
       return self.auth_tokens
    def get_auth_key(self):
        return self.Auth_key
    def get_token(self):
        return self.auth_tokens
    def download_url(self,name):
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        base_url  = 'http://%s/%s' % (bucket_domain, name )
        private_url =auth.private_download_url(base_url, expires=3600)
        return private_url


