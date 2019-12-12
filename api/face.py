# coding= utf-8

import base64

from flask import Blueprint, request, redirect

from service.face_service import FaceService
from util.form.face_form import FaceRegister, FaceSearch, UserSearchFace
from util.form.form import validate_form
from util.resp_util import ResponseUtil
from config.limiter import limiter
from config.config import PAGE_LIMIT, FILE_EXT, FACE_FRONT

face = Blueprint('face', __name__)

face_service = FaceService()


@limiter.limit("2 per second")
@face.route("/add", methods=['POST'])
def face_register():
    """
    向指定人脸组添加人脸
    @:param
    {
        "uer_id": "",
        "face_name": "",
    }
    :return:
    {"msg": "success", "code": 0, "data": null}
    """
    form = FaceRegister(request.form)
    try:
        validate_form(form)
        file_base64, filename = upload_file2base64(request.files)
        face_service.face_add(form.data, file_base64, filename)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("2 per second")
@face.route("/search", methods=['POST'])
def face_search():
    """
    在指定组中搜索人脸
    @:param
    {
        "user_id": 10,
    }
    :return:
    {"msg": "success", "code": 0, "data": null}
    """
    form = FaceSearch(request.form)
    try:
        # validate_form(form)
        str = request.json
        # file_base64, _ = upload_file2base64(request.files)
        uid = str.get('uid')
        file_base64 = str.get('base64_code')
        face_service.face_search(uid, file_base64)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("10 per second")
@face.route("/get")
def get_all_by_one():
    """
    获取某些组(user_ids)下的所有face
    @:param
    {
        "user_ids": [10, 15],
        "page": 1
    }
    :return:
    """
    form = UserSearchFace.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        user_ids = form.data.get('user_ids')
        if len(user_ids) > PAGE_LIMIT:
            raise Exception('最大查询10个id')
        res = face_service.get_face_by_user_ids(form.data)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=e.message)
    return ResponseUtil.success_response(data=res, msg='success')

@limiter.limit("10 per second")
@face.route("/redirect/check")
def redirect_check():
    uid = request.cookies.get('login_token').split('-')[0]
    return redirect(FACE_FRONT + '#/check/%s' % uid)



def upload_file2base64(files):
    if 'file' not in files:
        raise Exception('缺少人像图片')
    file = files['file']
    if file.filename == '':
        raise Exception('图片名称不能为空')
    if file.filename.split('.')[-1] not in FILE_EXT:
        raise Exception('仅支持jpg,jpeg,png类型的文件')
    file_base64 = base64.b64encode(file.read())
    return file_base64, file.filename
