from Database.tables import UserImage
from Userinfo.Usermodel import decode_base64
from Database.models import get_db
from FileHandler.Upload import AuthKeyHandler

def wechat_user_model_simply(user):

    db = get_db()
    headimg = db.query(UserImage).filter(UserImage.UIuid == user.Uid, UserImage.UIvalid == 1).one()
    auth = AuthKeyHandler()
    retdata = dict(
        Uid = user.Uid,
        #Utel = decode_base64(user.Utel),
        Ualais = user.Ualais,
        Usex = int(user.Usex),
        headimg=auth.download_abb_url(headimg.UIurl)
    )
    return retdata
def wechat_user_tel_model_simply(user):
    db = get_db()
    headimg = db.query(UserImage).filter(UserImage.UIuid == user.Uid, UserImage.UIvalid == 1).one()
    auth = AuthKeyHandler()
    retdata = dict(
        Uid=user.Uid,
        Utel = decode_base64(user.Utel),
        Ualais=user.Ualais,
        Usex=int(user.Usex),
        headimg=auth.download_abb_url(headimg.UIurl)
    )
    return retdata

def wechat_user_model_select_simply(user):
    db = get_db()
    headimg = db.query(UserImage).filter(UserImage.UIuid == user.Uid, UserImage.UIvalid == 1).one()
    auth = AuthKeyHandler()
    retdata = dict(
        Uid = user.Uid,
        Utel = decode_base64(user.Utel),
        Ualais = user.Ualais,
        Usex = int(user.Usex),
        headimg=auth.download_abb_url(headimg.UIurl)
    )
    return retdata

