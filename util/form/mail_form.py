# coding=utf-8
from wtforms import Form, StringField, validators


class RegisterCode(Form):
    """
    自定义邮箱验证
    """
    email = StringField(u'邮箱', [validators.Length(min=6, max=32), validators.Email(message=u'邮箱格式不正确'),
                                validators.required()])
