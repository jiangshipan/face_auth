# coding= utf-8
from config.config import PAGE_LIMIT
from config.db import db
from model.record import Record
from util.face_auth_utils import Singleton


class RecordDao(object):

    __metaclass__ = Singleton


    @staticmethod
    def insert(record):
        db.session.add(record)

    @staticmethod
    def get_record_by_user_id(user_id, page, query_filters):
        filters = [Record.user_id == user_id]
        pro_class = query_filters.get('pro_class')
        if pro_class:
            filters.append(Record.pro_class == pro_class)
        records = Record.query.filter(*filters).all()
        # total可维护到redis中
        total = len(records)
        return Record.query.filter(*filters).order_by(Record.create_time.desc()).limit(PAGE_LIMIT)\
            .offset((page - 1) * PAGE_LIMIT).all(), total
