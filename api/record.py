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

def build_filters(params):
    filter_fields = ['pro_class']
    filters = {}
    for item in filter_fields:
        if params.get(item):
            filters.update({
                item: params.get(item)
            })
    return filters