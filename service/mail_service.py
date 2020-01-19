# coding= utf-8
from config.mail import mail
from flask_mail import Message
from config import config
from config.db import app
from client.redis_client import redis_client
from concurrent.futures import ThreadPoolExecutor

from dao.email_dao import EmailDao
from util.face_auth_utils import FaceAuthUtils, Singleton

executor = ThreadPoolExecutor(5)


class MailService(object):
    """
    邮箱服务
    """

    __metaclass__ = Singleton


    def send_register_code(self, email):
        """
        发送注册码 有效期10分钟
        :param email:
        :return:
        """
        email_entity = EmailDao.get_email(email)
        if email_entity:
            raise Exception("the email is exist")
        code = FaceAuthUtils.generate_code()
        redis_client.set(email, code, ex=10 * 60)
        msg = self.create_msg(email, code)
        self.async_send(msg)

    def create_msg(self, email, code):
        msg = Message(subject='欢迎注册face_auth', sender=config.MAIL_USERNAME, recipients=[email])
        msg.html = '<h1>【face_auth】您的注册码：' + code + ', 请于10分钟内注册。</h1>'
        return msg

    def async_send(self, msg):
        """
        异步构建任务
        :return:
        """
        executor.submit(self.send, msg)

    def send(self, msg):
        """
        发送邮件
        :param msg:
        :return:
        """
        with app.app_context():
            mail.send(msg)
            print 'success'

    def send_msg_to_all(self, title, msg, email):
        """
        发送msg给所有email
        :return:
        """
        message = Message(subject=title, sender=config.MAIL_USERNAME, recipients=[email])
        message.html = '<p>' + msg + '<p>'
        self.async_send(message)

if __name__ == '__main__':
    # msg = Message(subject='test', sender=config.MAIL_USERNAME, recipients=['1320740751@qq.com'])
    # with app.app_context():
    #     mail.send(msg)
    mail_service = MailService()
    mail_service.send_msg_to_all('test', 'test', '1320740751@qq.com')
