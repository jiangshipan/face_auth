# coding= utf-8
from dao.record_dao import RecordDao
from dao.user_dao import UserDao


class RecordService(object):

    def get_record(self, user_id, page, filters):
        records = RecordDao.get_record_by_user_id(user_id, page, filters)
        if not records:
            return []
        # 根据user_id 获取教师姓名 不需要判断。 被禁用的teacher无法进入系统
        user = UserDao.get_user_by_user_id(user_id)
        res = []
        for record in records:
            res.append({
                'id': record.id,
                'belong': user.username,
                'pro_class': record.pro_class,
                'unchecked': record.unchecked,
                'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return res
