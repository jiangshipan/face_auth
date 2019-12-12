# coding= utf-8
from sqlalchemy import func

from config.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, doc=u'用户唯一标识')
    username = db.Column(db.String(32), nullable=False, doc=u'用户名')
    password = db.Column(db.String(32), nullable=False, doc=u'密码')
    nickname = db.Column(db.String(32), nullable=False, default=u'', doc=u'昵称')
    salt = db.Column(db.String(4), nullable=False, doc=u'加密盐')
    status = db.Column(db.Integer, nullable=False, default=0, doc=u'状态 0 启用 1 禁用')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'创建时间')

    @staticmethod
    def create(username, password, salt):
        user = User()
        user.username = username
        user.password = password
        user.salt = salt
        return user


