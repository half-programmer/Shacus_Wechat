# -*- coding: utf-8 -*-

import tornado.web

from Database import models
'''
@author: 黄鑫晨
'''

class BaseHandler(tornado.web.RequestHandler):

    @property  # python装饰器把一个方法变成属性调用
    def db(self):
        return self.application.db

    # def initialize(self):
    #     self.session = models.DB_Session()

    def on_finish(self):
        self.db.close()





