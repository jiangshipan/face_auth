# coding= utf-8
import json

from config.enum import FaceStatus
from dao.face_dao import FaceDao
from dao.record_dao import RecordDao
from dao.user_dao import UserDao
from util.face_auth_utils import Singleton


class RecordService(object):

    __metaclass__ = Singleton


    def get_record(self, user_id, page, filters):
        records, total = RecordDao.get_record_by_user_id(user_id, page, filters)
        if not records:
            return {'data': [], 'total': 0}
        # 根据user_id 获取教师姓名 不需要判断。 被禁用的teacher无法进入系统
        user = UserDao.get_user_by_user_id(user_id)
        res = {}
        data = []
        for record in records:
            unchecked = json.loads(record.unchecked)
            data.append({
                'id': record.id,
                'belong': user.username,
                'pro_class': record.pro_class,
                'unchecked': unchecked.get('data'),
                'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        res.update({
            'data': data,
            'total': total
        })
        return res


    def get_real_record_by_class(self, user_id, pro_class):
        """
        获取某老师下某班级实时签到记录
        :param user_id:
        :param pro_class:
        :return:
        """
        record = RecordDao.get_lastest_record_by_class(user_id, pro_class)
        if not record:
            return []
        record_content = json.loads(record.record)
        # 获取班级下未签到的人
        unchecked = []
        face_infos = FaceDao.get_by_class_user_id(pro_class, user_id, FaceStatus.UNCHECK)
        for face_info in face_infos:
            unchecked.append(face_info.face_name)
        res = {
            'checked': record_content.get('data'),
            'unchecked': unchecked
        }
        return res
