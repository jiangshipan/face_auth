# coding= utf-8

import base64

from flask import Blueprint, request, redirect

from service.face_service import FaceService
from util.form.face_form import FaceRegister, FaceSearch
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
    form = FaceRegister.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        face_service.face_add(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("2 per second")
@face.route("/search", methods=['POST'])
def face_search():
    """
    在指定组中搜索人脸（签到）
    @:param
    {
        "user_id": 10,
    }
    :return:
    {"msg": "success", "code": 0, "data": null}
    """
    form = FaceSearch.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        face_service.face_search(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("10 per second")
@face.route("/get")
def get_all_by_one():
    """
    获取某个用户(教师)下的学生列表
    @:param
    page
    :return:
    """
    try:
        user_id = request.cookies.get('login_token').split('-')[0]
        page = request.args.get('page', 1)
        filters = build_filters(request.args)
        res = face_service.get_face_by_user_id(user_id, filters, page)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=e.message)
    return ResponseUtil.success_response(data=res, msg='success')


@limiter.limit("10 per second")
@face.route("/redirect/check")
def redirect_check():
    uid = request.cookies.get('login_token').split('-')[0]
    return redirect(FACE_FRONT + '#/check/%s' % uid)


@limiter.limit("10 per second")
@face.route("/redirect/input")
def redirect_input():
    uid = request.cookies.get('login_token').split('-')[0]
    return redirect(FACE_FRONT + '#/input/%s' % uid)


@limiter.limit("10 per second")
@face.route("/init")
def init_face():
    """
    初始化某个班的签到状态
    :return:
    """
    try:
        stu_class = request.args.get('stu_class')
        if not stu_class:
            raise Exception("请输入班级")
        user_id = request.cookies.get('login_token').split('-')[0]
        face_service.init_face(stu_class, user_id)
        return ResponseUtil.success_response(msg='success')
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)


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


def build_filters(params):
    filter_fields = ['face_name', 'stu_class', 'status']
    filters = {}
    for item in filter_fields:
        if params.get(item):
            filters.update({
                item: params.get(item)
            })
    return filters
