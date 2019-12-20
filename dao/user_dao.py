# coding= utf-8
from config.db import db
from model.user import User
from config.enum import UserStatus
from util.face_auth_utils import Singleton


class UserDao(object):

    __metaclass__ = Singleton


    @staticmethod
    def insert(user):
        db.session.add(user)
        db.session.flush([user])


    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(User.username == username, User.status == UserStatus.NORMAL).first()

    @staticmethod
    def get_user_by_user_id(user_id):
        return User.query.filter(User.id == user_id, User.status == UserStatus.NORMAL).first()
