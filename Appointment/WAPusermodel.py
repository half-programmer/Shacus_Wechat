from Userinfo.Usermodel import decode_base64


def wechat_user_model_simply(user):
    retdata = dict(
        Uid = user.Uid,
        #Utel = decode_base64(user.Utel),
        Ualais = user.Ualais,
        Usex = int(user.Usex),
    )
    return retdata

def wechat_user_model_select_simply(user):
    retdata = dict(
        Uid = user.Uid,
        Utel = decode_base64(user.Utel),
        Ualais = user.Ualais,
        Usex = int(user.Usex),
    )
    return retdata

