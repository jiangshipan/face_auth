# coding= utf-8
from config.db import db
from config.enum import FaceStatus
from model.face import Face
from config.config import PAGE_LIMIT
from util.face_auth_utils import Singleton
from sqlalchemy import func


class FaceDao(object):
    __metaclass__ = Singleton

    @staticmethod
    def insert(user):
        db.session.add(user)
        db.session.flush([user])

    @staticmethod
    def get_by_user_id_and_face_name(user_id, face_name):
        return Face.query.filter(Face.user_id == user_id, Face.face_name == face_name, Face.status != FaceStatus.FORBID) \
            .first()

    @staticmethod
    def get_face_by_user_id(user_id, page, query_filters):
        filters = [Face.user_id == user_id]
        face_name = query_filters.get('face_name')
        face_class = query_filters.get('stu_class')
        status = query_filters.get('status')
        if face_name:
            filters.append(Face.face_name == face_name)
        if face_class:
            filters.append(Face.face_class == face_class)
        if status:
            filters.append(Face.status == status)
        else:
            filters.append(Face.status != FaceStatus.FORBID)
        faces = Face.query.filter(*filters).all()
        total = len(faces)
        return Face.query.filter(*filters).limit(PAGE_LIMIT).offset((page - 1) * PAGE_LIMIT).all(), total

    @staticmethod
    def get_face_by_face_id(face_id):
        return Face.query.filter(Face.id == face_id, Face.status != FaceStatus.FORBID).first()

    @staticmethod
    def get_by_class_user_id(stu_class, user_id, status):
        """
        根据stu_class, user_id获取未签到的人
        :param status:
        :param stu_class:
        :param user_id:
        :return:
        """
        return Face.query.filter(Face.user_id == user_id, Face.face_class == stu_class,
                                 Face.status == status).all()

    @staticmethod
    def get_by_class_user_id2(stu_class, user_id, oepn_check):
        return Face.query.filter(Face.user_id == user_id, Face.face_class == stu_class,
                                 Face.open_check == oepn_check).all()

    @staticmethod
    def get_class_by_user_id(user_id):
        return Face.query.filter(Face.user_id == user_id, Face.status != FaceStatus.FORBID) \
            .with_entities(Face.face_class, Face.open_check).all()
