# -*— coding:utf-8 -*-
'''
author:黄鑫晨
2016.10.28
'''
import sys
sys.path.append("..")
from Database.models import get_db
from BaseHandlerh import BaseHandler
from Database.tables import User, NewChoosed


class NewChoosedHandler(object):

    def init_table(self):
        db = get_db()
        users = db.query(User).filter(User.Uvalid == 1).all()
        for user in users:
            uid = user.Uid
            try:
                choosed_exist = db.query(NewChoosed).filter(NewChoosed.uid == uid).one()
            except Exception, e:
                new_choosed_entry = NewChoosed(
                    uid=user.Uid,
                    choosed=0
                )
                db.merge(new_choosed_entry)
                try:
                    db.commit()
                except Exception, e:
                    print e
new_choosed_handler = NewChoosedHandler()
new_choosed_handler.init_table()

