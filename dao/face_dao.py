# coding= utf-8
from config.db import db
from config.enum import FaceStatus
from model.face import Face
from config.config import PAGE_LIMIT


class FaceDao(object):

    @staticmethod
    def insert(user):
        db.session.add(user)
        db.session.flush([user])

    # @staticmethod
    # def update(user):
    #     db.session.flush([user])

    @staticmethod
    def get_by_user_id_and_face_name(user_id, face_name):
        return Face.query.filter(Face.user_id == user_id, Face.face_name == face_name, Face.status != FaceStatus.FORBID) \
            .first()

    @staticmethod
    def get_face_by_user_id(user_id, page):
        return Face.query.filter(Face.user_id == user_id, Face.status != FaceStatus.FORBID).limit(PAGE_LIMIT).offset(page - 1).all()

    @staticmethod
    def get_face_by_face_id(face_id):
        return Face.query.filter(Face.id == face_id, Face.status != FaceStatus.FORBID).first()