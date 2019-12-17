# coding= utf-8
from dao.record_dao import RecordDao


class RecordService(object):

    def get_record(self, user_id, page, filters):
        records = RecordDao.get_record_by_user_id(user_id, page, filters)
        if not records:
            return []
        res = []
        for record in records:
            res.append({
                'id': record.id,
                'user_id': record.user_id,
                'pro_class': record.pro_class,
                'unchecked': record.unchecked,
                'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return res
