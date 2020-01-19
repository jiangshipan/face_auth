# coding= utf-8
import json
from datetime import datetime, timedelta

from apscheduler.triggers.cron import CronTrigger

from config.enum import RecordType
from dao.email_dao import EmailDao
from dao.record_dao import RecordDao
from collections import defaultdict
from dao.user_dao import UserDao
from service.mail_service import MailService

# 解决ascii和unicode冲突的问题
import sys

reload(sys)
sys.setdefaultencoding('utf8')

mail_service = MailService()


def send_day_record():
    """
    发送日报
    :return:
    """
    send_record(RecordType.DAY)


def send_week_record():
    """
    发送周报
    :return:
    """
    send_record(RecordType.WEEK)


def send_month_record():
    """
    发送日报
    :return:
    """
    send_record(RecordType.MONTH)


def send_record(type):
    """
    发送日/周/月报 - 各老师或班级的签到记录
    :param type:
    :return:
    """
    global create_time
    mark = ''
    if type == RecordType.DAY:
        create_time = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S'),
        mark = u'日报'
    elif type == RecordType.WEEK:
        create_time = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d %H:%M:%S'),
        mark = u'周报'
    elif type == RecordType.MONTH:
        create_time = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d %H:%M:%S'),
        mark = u'月报'
    # 获取最近一周的签到记录
    query_filter = {
        'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'create_time': create_time
    }
    records = RecordDao.get_all_record_by_filters(query_filter)
    user_records = defaultdict(list)
    for record in records:
        user_records[record.user_id].append(record)
    for k, v in user_records.items():
        email_info = EmailDao.get_email_by_user_id(k)
        if not email_info:
            continue
        email = email_info.email
        user = UserDao.get_user_by_user_id(k)
        if not user:
            continue
        title = '%s: %s ~ %s 之间的签到记录' % (mark, query_filter.get('end_time'), query_filter.get('end_time'))
        head_text = '%s 你好, face_auth自动推送签到记录<br>' % user.username.encode('utf-8')
        msg = []
        msg.append(head_text)
        for record in v:
            unchecked = json.loads(record.unchecked).get('data')
            unchecked_people = ''.join(unchecked)
            create_time = record.create_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time = record.end_time.strftime('%Y-%m-%d %H:%M:%S')
            if not unchecked_people:
                unchecked_people = u'无'
            msg.append('班级: %s, 未签到的人: %s, 签到时间范围: %s ~ %s <br>' % (record.pro_class, unchecked_people,
                                                                    create_time, end_time))
        mail_service.send_msg_to_all(title, ''.join(msg), email)
    print '%s发送完成, 发送时间:%s' % (mark, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    # 每天6点执行该方法
    scheduler.add_job(send_day_record, CronTrigger.from_crontab('0 6 * * *'))
    scheduler.add_job(send_week_record, CronTrigger.from_crontab('0 6 * * 1'))
    scheduler.add_job(send_month_record, CronTrigger.from_crontab('0 6 1 1-12 *'))
    scheduler.start()
