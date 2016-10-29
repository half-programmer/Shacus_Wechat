# -*-coding: utf-8 -*-

'''
@author :兰威
@datatime: 2016.10.11
@type:生成和识别session_id
'''

from hashlib import sha1

import os, time

session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()


class SessionHandler(object):
    _id = None
    _prefix = "_session:"
    _skip = ["_redis", "_request", "_id", "lastActive", "_prefix", "session_lifetime"]

    def __init__(self, request, redis, session_lifetime=60 * 60 * 24):
        self._request = request
        self._redis = redis
        self.session_lifetime = session_lifetime
        self.init_session()

    def init_session(self):
        """初始化"""
        _id = self._request.get_secure_cookie("session_id")
        if not _id:
            _id = session_id()
        else:
            if not self._redis.exists(_id):
                _id = session_id()
        self._request.set_secure_cookie("session_id", _id)
        self._id = _id

    def __getattr__(self, name):
        if name in self._skip:
            return object.__getattr__(self, name)
        else:
            return self._redis.hget(self._id, name)

    def __setattr__(self, name, value):
        if name in self._skip:
            object.__setattr__(self, name, value)
        else:
            self.init_session()
            self._redis.hset(self._id, name, value)
            self._redis.expire(self._id, self.session_lifetime)

    def __delattr__(self, name):
        if name in self._skip:
            object.__delattr__(self, name)
        else:
            return self._redis.hdel(self._id, name)


__all__ = ["SessionHandler", "session_id"]


