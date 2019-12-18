# coding= utf-8
from flask import Blueprint, request, make_response

from service.mail_service import MailService
from service.user_service import UserService
from util.form.mail_form import RegisterCode
from util.resp_util import ResponseUtil
from util.form.user_form import UserRegister
from util.form.form import validate_form
from config.limiter import limiter

user = Blueprint('user', __name__)

user_service = UserService()
email_service = MailService()


@limiter.limit("10 per second")
@user.route("/login")
def login():
    """
    登陆接口
    @:param username, password
    :return:
    {"msg": "34e3f953ee814a66a62b2cc2c02b1968", "code": 0, "data": null}
    """
    username = request.args.get('username')
    password = request.args.get('password')
    try:
        msg = user_service.user_login(username, password)
        resp = make_response('{"msg": "success", "code": 0, "data": null}')
        resp.set_cookie("login_token", msg, max_age=1 * 3600 * 24)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return resp


@limiter.limit("10 per second")
@user.route("/reg", methods=['POST'])
def register():
    """
    注册接口
    @:param
    {"username":"jiangsshipan","password":"19"}
    :return:
    {"msg":"success","code":1,"data":""}
    """
    form = UserRegister.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        user_service.user_register(form.data)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("10 per second")
@user.route("/code", methods=['POST'])
def register_code():
    """
    发送验证码接口
    @:param email
    :return:
    {"msg": "success", "code": 0, "data": null}
    """
    form = RegisterCode.from_json(formdata=request.json, meta={'locales': ['zh_CN', 'zh']})
    try:
        validate_form(form)
        email_service.send_register_code(form.data.get('email'))
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')


@limiter.limit("10 per second")
@user.route("/logout")
def logout():
    """
    用户注销
    :return:
    """
    user_id = request.cookies.get('login_token').split('-')[0]
    try:
        user_service.logout(user_id)
    except Exception as e:
        return ResponseUtil.error_response(msg=e.message)
    return ResponseUtil.success_response(msg='success')
