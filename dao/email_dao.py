# coding= utf-8
from config.db import db
from model.email import Email
from util.face_auth_utils import Singleton


class EmailDao(object):

    __metaclass__ = Singleton


    @staticmethod
    def insert(email):
        db.session.add(email)
        db.session.flush([email])


    @staticmethod
    def get_email(email):
        return Email.query.filter(Email.email == email).first()