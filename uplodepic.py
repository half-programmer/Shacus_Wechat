# -*-coding: utf-8 -*-
__author__='兰威'
import hashlib
import io
import  json

from PIL import Image

from  BaseHandlerh import BaseHandler


class UploadException(RuntimeError):
    def __init__(self,code,content):
        self.code=code
        self.content=content

class upload(BaseHandler):
    def post(self):
        global allfilepath  # 总图片地址
        allfilepath = ''
        upload_path = 'localhost:8000/activity/commit'
        save_path = 'activitypicture'
        retjson = {'code': 200, 'content': 'ok'}  # 返回json
        try:
            file_metas=self.request.files['file']

            if file_metas:
                for meta in file_metas:
                    filename=meta['filename']
                    suffixes=filename.split('.')[-1:][0]
                    if suffixes not in ['jpg','png']:
                        raise UploadException(401,u"文件格式不支持")
                    img=Image.open(io.BytesIO(meta['baby']))
                    shaobj = hashlib.md5()
                    shaobj.update(meta['body'])  # 获得图片hash值
                    filehash = shaobj.hexdigest()
                    filepath = save_path + '/' + filehash + '.jpg'
                    database_path = upload_path + '/' + filehash + '.jpg'
                    thumbpath = save_path + '/' + filehash + 'thumb_' + '.jpg'
                    img.save(filepath, 'JPEG')
                    img.thumbnail((100, 100), resample=1)  # 缩略图
                    img.save(thumbpath, 'jpeg')
                    allfilepath += thumbpath + ';' + filepath + ';'  # 缩略图和原图存储
                    retjson['content'] = database_path
            else:
                retjson['code'] = 501
                retjson['content'] = u'图片为空'
        except UploadException,e:
            retjson['code']=e.code
            retjson['content']=e.content
        except Exception,e:
            retjson['code']=500
            retjson['content']=u"系统错误"
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))  # ensure_ascii:允许中文