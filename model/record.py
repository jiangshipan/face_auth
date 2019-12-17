# coding= utf-8
from config.db import db
from sqlalchemy import func

class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True, doc=u'签到记录id')
    user_id = db.Column(db.Integer, nullable=False, default=0, doc=u'绑定用户id')  # 用户是一个组（此系统为老师）
    pro_class = db.Column(db.String(32), nullable=False, doc=u'专业班级')
    unchecked = db.Column(db.Text, nullable=False, default='', doc=u'未签到的人')
    create_time = db.Column(db.DateTime, nullable=False, default=func.now(), doc=u'创建时间')


    @staticmethod
    def create(user_id, pro_class, unchecked):
        record = Record()
        record.user_id = user_id
        record.pro_class = pro_class
        record.unchecked = unchecked
        return record
