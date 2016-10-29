# -*-coding: utf-8 -*-
'''
@author: 兰威
'''


from BaseHandlerh import BaseHandler

class ImageCallback(BaseHandler):
    def post(self):
        print('\n---------headers\n')
        print (self.request.headers)
        print('\n---------uri\n')
        print (self.request.uri)
        print ('\n--------youip\n')
        print (self.request.remote_ip)