# -*- coding:utf-8 -*-
'''
@author: 兰威
'''
from Database.models import get_db
from Database.tables import UserLike, ActivityLike, ActivityEntry, Activity, Verification, UCinfo, ActivityImage, \
    AppointmentInfo, AppointEntry, AppointLike, Appointment, AppointmentImage, User, RankScore, CourseLike, Usercourse, \
    UserImage, Image, Favorite

db = get_db()
items  = db.query(Favorite).all()
for item in items:
    db.delete(item)
db.commit()

items = db.query(UserLike).all()
for item in items:
    db.delete(item)
db.commit()
items  = db.query(ActivityLike).all()
for item in items:
    db.delete(item)
db.commit()
items  = db.query(ActivityEntry).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(Verification).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(UCinfo).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(ActivityImage).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(Activity).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(AppointmentInfo).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(AppointEntry).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(AppointLike).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(AppointmentImage).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(Appointment).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(RankScore).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(CourseLike).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(Usercourse).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(UserImage).all()
for item in items:
    db.delete(item)
db.commit()
items  = db.query(Image).all()
for item in items:
    db.delete(item)
db.commit()

items  = db.query(User).all()
for item in items:
    db.delete(item)
db.commit()
