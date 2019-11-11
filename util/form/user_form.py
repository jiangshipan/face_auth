# coding=utf-8
from wtforms import Form, StringField, validators


class UserRegister(Form):
    """
    自定义注册Form
    """
    username = StringField(u'用户名', [validators.Length(min=4, max=32), validators.required()])
    password = StringField(u'密码', [validators.Length(min=4, max=32), validators.required()])
    email = StringField(u'邮箱', [validators.Length(min=6, max=32), validators.Email(message=u'邮箱格式不正确'),
                                validators.required()])
    code = StringField(u'注册码', [validators.Length(min=6, max=6), validators.required()])



