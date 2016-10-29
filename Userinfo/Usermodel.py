# coding=utf-8
import base64

from Database.models import get_db
from Database.tables import UserImage, Image
from FileHandler.Upload import AuthKeyHandler
from Database.models import get_db
from FileHandler.Upload import AuthKeyHandler
#from Userinfo.Ufuncs import Ufuncs
'''
@author: 黄鑫晨 兰威
'''

def userinfo_smply(u_info, u_change_info):
    '''

    Args:
        u_info:
        u_change_info:
    返回个人简单信息
    Returns:

    '''
    auth = AuthKeyHandler()
    user_headimages = get_db().query(UserImage).filter(UserImage.UIuid == u_info.Uid).all()
    userimg = []
    for user_headimage in user_headimages:
        exist = get_db().query(Image).filter(Image.IMid == user_headimage.UIimid, Image.IMvalid == 1).all()
        if exist:
            userimg = user_headimage
            break;
    ret_info = {'uid': u_info.Uid, 'ualais': u_info.Ualais, 'ulocation': u_info.Ulocation,
                     'utel': u_info.Utel, 'uname': u_info.Uname, 'umailbox': u_info.Umailbox,
                     'ubirthday': u_info.Ubirthday, 'uscore': u_info.Uscore, 'usex': u_info.Usex,
                     'usign': u_info.Usign, 'uimage': auth.download_url(userimg.UIurl), 'ulikeN': u_change_info.UClikeN,
                     'ulikedN': u_change_info.UClikedN, 'uapN': u_change_info.UCapN,
                     'uphotoN': u_change_info.UCphotoN, 'ucourseN': u_change_info.UCcourseN,
                     'umomentN': u_change_info.UCmomentN}
    return ret_info

def Model_daohanglan(imgurl,weburl):
    dh_json = {'imgurl':imgurl, 'weburl':weburl}
    return dh_json

def user_login_fail_model():
    user_model = dict(
        id='0',
        phone='wu',
        nickName='wu',
        realName='wu',
        sign='wu',
        sex='wu',
        score='wu',
        location='wu',
        birthday='wu',
        registTime='wu',
        mailBox='wu',
        headImage='wu',
        auth_key='wu'
    )
    return user_model

def get_user_detail_from_user(user):
    try:
        if user.Ubirthday:
            Ubirthday = user.Ubirthday.strftime('%Y-%m-%d %H:%M:%S'),
        else:
            Ubirthday = ''
    except Exception, e:
        print e
        Ubirthday = ''
    user_model = dict(
        id=user.Uid,
        phone=user.Utel,
        nickName=user.Ualais,
        realName=user.Uname,
        sign=user.Usign,
        sex=user.Usex,
        score=user.Uscore,
        location=user.Ulocation,
        birthday=Ubirthday,
        registTime=user.UregistT.strftime('%Y-%m-%d %H:%M:%S'),
        mailBox=user.Umailbox,
        headImage=Ufuncs.get_user_headimage_intent_from_userid(user.Uid),
        auth_key=user.Uauthkey,
        chattoken=user.Uchattoken
    )
    return user_model


def decode_base64(data):
    """Decode base64, padding being optional.
:param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
"""
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)

def wechat_user_model_simply(user):
    retdata = dict(
        Uid = user.Uid,
        Utel = decode_base64(user.Utel),
        Ualais = user.Ualais,
        Usex = int(user.Usex),
    )
    return retdata