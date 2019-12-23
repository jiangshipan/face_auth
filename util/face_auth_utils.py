# coding= utf-8
import random
import base64
import traceback
import uuid
import os
from datetime import datetime
from config.config import FILE_PATH, FILE_DIR, LOG_NAME, VISIT_DIR


class FaceAuthUtils(object):
    """
    公共工具类
    """

    @staticmethod
    def generate_code():
        """
        获取6位随机注册码
        :return:
        """
        code = []
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(6):
            code.append(str(random.choice(nums)))
        return ''.join(code)

    @staticmethod
    def base642imag(file_base64):
        """
        根据base64码上传图片
        :param file_base64: 图片的base64编码
        :return:
        """
        # 随机生成文件名
        filename = ''.join(str(uuid.uuid4()).split('-')) + '.jpg'
        file_choice = random.choice(FILE_DIR)
        file_dir = FILE_PATH + file_choice
        file_url = file_dir + '/' + filename
        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_url, 'wb') as f:
                f.write(base64.b64decode(file_base64))
        except Exception as e:
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise Exception('文件上传失败, 原因:' % e.message)
        return VISIT_DIR + file_choice + '/' + filename

    @staticmethod
    def save_exception(exception):
        with open(LOG_NAME, "a+") as f:
            content = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n' + exception
            f.write(content + '\n')


class Singleton(type):
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args)
        return cls._inst[cls]


if __name__ == '__main__':
    pass
