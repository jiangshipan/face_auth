# coding= utf-8
from config.db import db
from model.user import User
from config.enum import UserStatus


class UserDao(object):

    @staticmethod
    def insert(user):
        db.session.add(user)
        db.session.flush([user])


    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(User.username == username, User.status == UserStatus.NORMAL).first()
