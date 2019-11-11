# coding= utf-8
import json


class ResponseUtil(object):

    @staticmethod
    def success_response(data=None, msg=u""):
        result = Resp(data, StatusCode.SUCCESS, msg).__dict__
        return json.dumps(result)

    @staticmethod
    def error_response(data=None, msg=u""):
        result = Resp(data, StatusCode.FAIL, msg).__dict__
        return json.dumps(result)


class Resp(object):
    """
    返回统一格式
    """

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg


class StatusCode(object):
    """
    统一错误码
    """
    # 成功
    SUCCESS = 0
    # 失败
    FAIL = 1
