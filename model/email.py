# coding= utf-8
from sqlalchemy import func

from config.db import db


class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True, doc=u'email唯一标识')
    user_id = db.Column(db.Integer, nullable=False, default=0, doc=u'用户id')
    email = db.Column(db.String(32), nullable=False, doc=u'邮箱')
    fix_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'绑定时间')

    @staticmethod
    def create(user_id, fix_email):
        email = Email()
        email.user_id = user_id
        email.email = fix_email
        return email



