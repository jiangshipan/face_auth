# coding= utf-8
import json
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
