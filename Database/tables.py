# -*- coding: utf-8 -*-


'''
@author: 黄鑫晨 兰威 王佳镭
'''

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,ForeignKey,DateTime,Boolean
from sqlalchemy.types import CHAR, Integer, VARCHAR,Boolean,Float
from sqlalchemy.sql.functions import func
from models import Base
import sys
reload(sys)

# from models import engine

# 每个类对应一个表
class User(Base): # 用户表   #添加聊天专用chattoken
    __tablename__ = 'User'

    Uid = Column(Integer, nullable=False, primary_key=True)  # 主键
    Upassword = Column(VARCHAR(64), nullable=False)
    Utel = Column(CHAR(32), nullable=False,unique=True)
    Ualais = Column(VARCHAR(24),nullable=False,unique=True)  # 昵称，可能为微信昵称
    Uname = Column(VARCHAR(24)) # 真实姓名
    Ulocation = Column(VARCHAR(128))
    Uopenid = Column(VARCHAR(128))
    Umailbox = Column(VARCHAR(32))  # 邮箱
    Ubirthday = Column(DateTime)
    Uscore = Column(Integer, default=0)
    UregistT = Column(DateTime(timezone=True), default=func.now())
    Usex = Column(Boolean, nullable=False)
    Usign = Column(VARCHAR(256))
    Usessionid = Column(VARCHAR(32))    #用于验证用户
    Uvalid = Column(Integer, nullable=False, default=1)



class Verification(Base):  # 短信验证码及生成用户auth_key时间
    __tablename__ = 'Verification'

    Vphone = Column(CHAR(11),primary_key=True) #
    Vcode = Column(CHAR(6),nullable=False)
    VT = Column(DateTime(timezone=True), default=func.now()) # 待测试是插入数据的时间还是最后一次更新该表的时间 （测试结果为第一次插入时间）


class Image(Base):
    __tablename__ = 'Image'

    IMid = Column(Integer,primary_key=True,nullable=False)
    IMvalid = Column(Boolean,default=1)
    IMT = Column(DateTime(timezone=True), default=func.now())
    IMname = Column(VARCHAR(128), nullable=False)


class UserImage(Base):
    __tablename__ = 'UserImage'

    UIuid = Column(Integer,ForeignKey("User.Uid", onupdate="CASCADE"))
    UIimid = Column(Integer,ForeignKey("Image.IMid", onupdate="CASCADE"), primary_key=True)
    UIurl = Column(VARCHAR(128))


class WCourse(Base):
    '''
    @author:黄鑫晨
    @name：教程表
    '''
    __tablename__ = "WCourse"
    WCid = Column(Integer,primary_key=True)
    WCurl = Column(VARCHAR(128), nullable=False)  # 链接
    WCintroduce = Column(VARCHAR(64))  # 教程简介
    WCimageurl = Column(VARCHAR(128), nullable=False)  # 封面图片
    WCtitle = Column(VARCHAR(32), nullable=False)  # 标题
    WCvalid = Column(Integer, nullable=False, default=1)


class WeAcToken(Base):
    '''
    用于存放微信accesstoken
    '''
    __tablename__ = 'WeAcToken'
    WACid = Column(Integer, primary_key=True)
    WACtoken = Column(VARCHAR(512))
    WACexpire = Column(Integer,nullable=False,default=0)


class WAppointment(Base):
    '''
    @author:兰威
    @name：约拍表
    '''
    __tablename__ = 'WAppointment'

    WAPid = Column(Integer, primary_key=True, nullable=False)
    WAPsponsorid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE')) #约拍请求发起者ID
    WAPtitle = Column(VARCHAR(24), nullable=False)  # 标题
    WAPlocation = Column(VARCHAR(128), nullable=False, default='')  # 地点描述
    WAPcontent = Column(VARCHAR(128), nullable=False, default='')  # 内容描述
    WAPfree = Column(Boolean)  # 0为免费，1为收费
    WAPtime = Column(VARCHAR(128), nullable=False, default='')  # 时间描述
    WAPcreateT = Column(DateTime(timezone=True), default=func.now())
    WAPtype = Column(Boolean, nullable=False, default=0)  # 约拍类型，模特约摄影师(1)或摄影师约模特(0)
    WAPvalid = Column(Boolean, default=1, nullable=False)
    WAPregistN = Column(Integer, nullable=False, default=0)
    WAPstatus = Column(Integer, nullable=False, default=0)  # 1为发布中，2为已确定约拍对象(进行中) 3为一方已结束 4为两方都结束


class WApImage(Base):
    __tablename__ = 'WApImage'

    WAPIapid = Column(Integer, ForeignKey("WAppointment.WAPid", onupdate="CASCADE"))
    WAPIimid = Column(Integer, ForeignKey("Image.IMid",onupdate="CASCADE"), primary_key=True)
    WAPIurl = Column(VARCHAR(128))


class WApInfo(Base):
    '''
    @author:黄鑫晨
    @name:约拍评论表，即每一个确定的约拍对应的表，选择人后在此加一项
    '''
    __tablename__ = "WApinfo"

    WAIid = Column(Integer, primary_key=True)
    WAImid = Column(Integer, ForeignKey('User.Uid', ondelete='CASCADE'))  # 模特的Id
    WAIpid = Column(Integer, ForeignKey('User.Uid', ondelete='CASCADE'))  # 摄影师的id
    WAImscore = Column(Integer, default=0)  # 模特获得的得分
    WAIpscore = Column(Integer, default=0)  # 摄影师获得的得分
    WAImcomment = Column(VARCHAR(128))  # 模特对摄影师的评论
    WAIpcomment = Column(VARCHAR(128))  # 摄影师对模特的评论
    WAImcommentT = Column(DateTime(timezone=True), default=func.now())  # 模特对摄影师的评论的时间
    WAIpcommentT = Column(DateTime(timezone=True), default=func.now())  # 摄影师对模特的评论的时间
    WAIappoid = Column(Integer, ForeignKey('WAppointment.WAPid', onupdate='CASCADE'))  # 约拍Id
    WAIvalid = Column(Boolean, default=1, nullable=False)

class WApFinish(Base):
    '''
    @author:兰威
    @name:约拍结束表
    '''
    __tablename__ = 'WApFinish'
    WAFid = Column(Integer, primary_key=True)
    WAFapid=Column(Integer, ForeignKey('WAppointment.WAPid', onupdate="CASCADE"))  # 约拍id
    WAFuid=Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))  # 报名人id
    WAFfinishT = Column(DateTime(timezone=True), default=func.now())  # 结束时间

class WAppointEntry(Base):
    '''
    @author:黄鑫晨
    @name:约拍报名表
    '''
    __tablename__ = "WAppointEntry"

    WAEid = Column(Integer, primary_key=True)
    WAEapid=Column(Integer, ForeignKey('WAppointment.WAPid', onupdate="CASCADE"))  # 约拍id
    WAEregisterID = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))  # 报名人id
    WAEvalid = Column(Boolean, nullable=False,default=1)  # 报名是否有效
    WAEchoosed = Column(Boolean, nullable=False,default=0)  # 是否被选中
    WAEregistT = Column(DateTime(timezone=True), default=func.now())  # 报名时间


class WActivity(Base):  # 活动表
    __tablename__ = 'WActivity'

    WACid = Column(Integer, nullable=False, primary_key=True)
    WACsponsorid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))  # 活动发起者
    WAClocation = Column(VARCHAR(128), nullable=False)  # 位置
    WACtitle = Column(VARCHAR(24), nullable=False)  # 活动的名称？确认长度
    WACstartT = Column(DateTime, nullable=False)  # 开始时间
    WACendT = Column(DateTime, nullable=False)  # 结束时间
    WACjoinT = Column(DateTime)  # 活动报名截止时间
    WACcontent = Column(VARCHAR(256), nullable=False)  # 活动介绍
    WACfree = Column(Boolean, default=1)  # 是否免费，默认为免费
    WACprice = Column(VARCHAR(64))  # 价格描述
    WACclosed = Column(Boolean, default=0, nullable=False)  # 活动是否已经结束,0为未结束，1为结束
    WACcreateT = Column(DateTime(timezone=True), default=func.now())  # 活动创建时间
    WACmaxp = Column(Integer,nullable=False, default=0)  # 活动最小人数
    WACminp = Column(Integer,nullable=False, default=100)  # 活动报名人上限
    WACregistN = Column(Integer,nullable=False, default=0)  # 报名人数
    WACstatus =Column(Integer, nullable=False, default=0)  # 活动状态，1为报名中，2为进行中，3为已结束
    WACvalid = Column(Boolean, nullable=False, default=1)  # 活动是否已经删除, 1为有效


class WAcImage(Base):
    __tablename__ = "WAcImage"

    WACIacid = Column(Integer, ForeignKey('WActivity.WACid',onupdate='CASCADE'))
    WACIimid = Column(Integer, ForeignKey('Image.IMid',onupdate='CASCADE'),primary_key=True)
    WACIurl = Column(VARCHAR(128))  # 活动图片链接


class WAcEntry(Base):  # 活动报名表
    '''
    @author:黄鑫晨
    @name:活动报名表
    '''
    __tablename__ = 'WAcEntry'

    WACEid = Column(Integer, primary_key=True)
    WACEacid = Column(Integer, ForeignKey('WActivity.WACid', onupdate='CASCADE'))  # 活动ID
    WACEregisterid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))  # 报名人ID
    WACEregistvalid = Column(Boolean, default=1)  # 报名是否有效
    WACEregisterT = Column(DateTime(timezone=True), default=func.now())  # 报名时间

class WApCompanions(Base):
    '''
    @author:黄鑫晨
    @name:约拍伴侣表
    '''
    __tablename__ = 'WApCompanions'
    WAPCid = Column(Integer, primary_key=True)
    WAPCname = Column(VARCHAR(64), nullable=False)   # 约拍伴侣名
    WAPCOrganintro = Column(VARCHAR(128), nullable=False)  # 组织/个人介绍
    WAPCServeintro = Column(VARCHAR(256), nullable=False)  # 提供服务介绍
    WAPCContact = Column(VARCHAR(128), nullable=False)  # 联系方式
    WAPCvalid = Column(Boolean, default=1, nullable=False)


class WApCompanionImage(Base):
    '''
    @author:黄鑫晨
    @name:约拍伴侣图片表
    '''
    __tablename__ = "WApCompanionImage"

    WAPCid = Column(Integer, ForeignKey('WApCompanions.WAPCid', onupdate='CASCADE'))
    WAPCimid = Column(Integer, ForeignKey('Image.IMid', onupdate='CASCADE'), primary_key=True)
    WAPCurl = Column(VARCHAR(128))  # 约拍伴侣图片链接
    WAPCvalid = Column(Boolean, default=1, nullable=False)


class Homepageimage(Base):
    '''
    author:wjl
    @name:个人主页的图片
    '''
    __tablename__ = 'Homepageimage'

    HPIid = Column(Integer, primary_key=True)
    HPuser = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))
    HPUimage = Column(Integer, ForeignKey('Image.IMid', onupdate='CASCADE'))
    HPimgurl = Column(VARCHAR(128))
    HPimgvalid = Column(Boolean,default=1,nullable=False)


class WAcAuth(Base):
    '''
    @author：黄鑫晨
    @name: 记录发布活动权限的表
    '''
    __tablename__ = 'WAcAuth'

    WAAid = Column(Integer, primary_key=True)
    WAauth = Column(VARCHAR(32), nullable=False)
    WAAacid = Column(Integer, ForeignKey('WActivity.WACid', onupdate='CASCADE'))  # 活动ID
    WAAused = Column(Boolean, nullable=False, default=0)  # 为0则未用， 1则用过


class NewChoosed(Base):
    '''
    @author: 黄鑫晨
    @introduction: 每次用户有新的被选中则记录, 登录后提示并清零
    '''
    __tablename__ = 'NewChoosed'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    choosed = Column(Boolean, nullable=False, default=0)  # 0为没有新选择， 1则有新选择


