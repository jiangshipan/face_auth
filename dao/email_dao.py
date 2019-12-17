# coding= utf-8
from config.db import db
from model.email import Email


class EmailDao(object):

    @staticmethod
    def insert(email):
        db.session.add(email)
        db.session.flush([email])


    @staticmethod
    def get_email(email):
        return Email.query.filter(Email.email == email).first()