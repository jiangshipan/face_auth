# coding= utf-8
import hashlib
import uuid

from dao.email_dao import EmailDao
from dao.user_dao import UserDao
from model.email import Email
from model.user import User
from config.db import db
from client.redis_client import redis_client


class UserService(object):
    """
    用户服务
    """

    def user_login(self, username, password):
        """
        用户登陆
        :param username:
        :param password:
        :return:
        """
        if not username or not password:
            raise Exception('username or password is empty')
        user = UserDao.get_user_by_username(username)
        if not user:
            raise Exception('user is not exist')
        if user.password != hashlib.md5(password + user.salt).hexdigest():
            raise Exception('password is not available')
        # 验证通过，分配token
        token = self.assign_token(user.id)
        return token

    def user_register(self, user_info):
        """
        用户注册
        :param user_info:
        :return:
        """
        email = user_info.get('email')
        code = user_info.get('code')
        real_code = redis_client.get(email)
        # 校验注册码
        if code != real_code:
            raise Exception('register code is incorrect')
        username = user_info.get('username')
        user = UserDao.get_user_by_username(username)
        if user:
            raise Exception('user has existed')
        salt = ''.join(str(uuid.uuid4()).split('-'))[:4]
        password = hashlib.md5(user_info.get('password') + salt).hexdigest()
        user = User.create(username, password, salt)
        try:
            UserDao.insert(user)
            # 邮箱绑定到用户
            email = Email.create(user.id, email)
            EmailDao.insert(email)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e.message)

    def assign_token(self, user_id):
        """
        分配token. 1天过期
        :param username:
        :return:
        """
        token = redis_client.get(user_id)
        if not token:
            token = str(user_id) + '-' + ''.join(str(uuid.uuid4()).split('-'))
            redis_client.set(user_id, token, ex=1 * 3600 * 24)
        return token

    def logout(self, user_id):
        redis_client.delete(user_id)