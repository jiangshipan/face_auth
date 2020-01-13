# coding= utf-8
from config.config import PAGE_LIMIT
from config.db import db
from model.record import Record
from util.face_auth_utils import Singleton
from config.enum import IS_OPEN


class RecordDao(object):
    __metaclass__ = Singleton

    @staticmethod
    def insert(record):
        db.session.add(record)

    @staticmethod
    def get_record_by_user_id(user_id, page, query_filters):
        filters = [Record.user_id == user_id, Record.status == IS_OPEN.YES]
        pro_class = query_filters.get('pro_class')
        create_time = query_filters.get('create_time')
        end_time = query_filters.get('end_time')
        if pro_class:
            filters.append(Record.pro_class == pro_class)
        if create_time:
            filters.append(Record.create_time >= create_time)
        if end_time:
            filters.append(Record.end_time <= end_time)
        records = Record.query.filter(*filters).all()
        # total可维护到redis中
        total = len(records)
        return Record.query.filter(*filters).order_by(Record.create_time.desc()).limit(PAGE_LIMIT) \
                   .offset((page - 1) * PAGE_LIMIT).all(), total

    @staticmethod
    def get_lastest_record_by_class(user_id, pro_class):
        # 一个班级只允许有一个不可查
        return Record.query.filter(Record.user_id == user_id, Record.pro_class == pro_class,
                                   Record.status == IS_OPEN.NO).first()

    @staticmethod
    def get_all_record_by_filters(query_filters):
        """
        根据筛选条件 选择符合的记录
        :return:
        """
        filters = [Record.status == IS_OPEN.YES]
        create_time = query_filters.get('create_time')
        end_time = query_filters.get('end_time')
        if create_time:
            filters.append(Record.create_time >= create_time)
        if end_time:
            filters.append(Record.end_time <= end_time)
        records = Record.query.filter(*filters).order_by(Record.create_time.desc()).all()
        return records

    @staticmethod
    def get_record_by_id(id):
        """
        根据id查询记录
        :param id:
        :return:
        """
        return Record.query.filter(Record.id == id).first()