# coding= utf-8
from config.db import db


class Face(db.Model):
    __tablename__ = 'face'

    id = db.Column(db.Integer, primary_key=True, doc=u'人脸id')
    user_id = db.Column(db.Integer, nullable=False, default=0, doc=u'绑定用户id')  # 用户是一个组。组下面管理很多人像
    face_name = db.Column(db.String(32), nullable=False, doc=u'人像名')
    face_url = db.Column(db.String(32), nullable=False, doc=u'人脸url')
    face_class = db.Column(db.String(32), nullable=False, doc=u'学生班级')
    status = db.Column(db.Integer, nullable=False, default=0, doc=u'状态 0 已签到 1 未签到 2 删除')

    @staticmethod
    def create(user_id, face_name, face_url, face_class):
        face = Face()
        face.user_id = user_id
        face.face_name = face_name
        face.face_url = face_url
        face.face_class = face_class
        return face
