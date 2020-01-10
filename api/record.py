# coding= utf-8

import json
from flask import Blueprint, request

from service.record_service import RecordService

from util.resp_util import ResponseUtil
from config.limiter import limiter

record = Blueprint('record', __name__)

record_service = RecordService()

@limiter.limit("10 per second")
@record.route("/get")
def get_reocrd():
    """
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    page = request.args.get('page', 1)
    try:
        filters = build_filters(request.args)
        res = record_service.get_record(user_id, int(page), filters)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=e.message)
    return ResponseUtil.success_response(data=res, msg='success')

@limiter.limit("10 per second")
@record.route("/get_now")
def get_real_record():
    """
    获取实时签到记录
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        pro_class = request.args.get('pro_class')
        if not pro_class:
            raise Exception('缺少班级参数')
        res = record_service.get_real_record_by_class(user_id, pro_class)
    except Exception as e:
        return ResponseUtil.error_response(data=[], msg=e.message)
    return ResponseUtil.success_response(data=res, msg='success')


def build_filters(params):
    filter_fields = ['pro_class']
    filters = {}
    for item in filter_fields:
        if params.get(item):
            filters.update({
                item: params.get(item)
            })
    return filters