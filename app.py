# coding= utf-8
from api.user import user
from api.face import face
from api.record import record
from client.redis_client import redis_client
from config.db import app
from flask import request
from util.resp_util import ResponseUtil


app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(face, url_prefix='/face')
app.register_blueprint(record, url_prefix='/record')

# 不进行校验的方法
ALLOW_METHOD = ['/user/login', '/user/reg', '/', '/user/code', '/face/add', '/face/search']


@app.before_request
def check_token():
    """
    校验身份
    :return:
    """
    method = str(request.url_rule)
    if not method or method not in ALLOW_METHOD:
        login_token = request.cookies.get('login_token')
        if not login_token:
            return ResponseUtil.error_response(msg='no access')
        user_id = login_token.split('-')[0]
        real_token = redis_client.get(user_id)
        if login_token != real_token:
            return ResponseUtil.error_response(msg='no access')
    return

@app.after_request
def cors(environ):
    """
    解决跨域
    :param environ:
    :return:
    """
    environ.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    environ.headers['Access-Control-Allow-Credentials'] = 'true'
    return environ

@app.route("/")
def hello():
    return ResponseUtil.error_response()


if __name__ == '__main__':
    # 开启服务
    app.run(debug=True)