# coding= utf-8
import random
import base64
import uuid
import os

from config.config import FILE_PATH, FILE_DIR


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
        filename = ''.join(str(uuid.uuid4()).split('-'))
        file_dir = FILE_PATH + random.choice(FILE_DIR)
        file_url = file_dir + '/' + filename
        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_url, 'wb') as f:
                f.write(base64.b64decode(file_base64))
        except Exception as e:
            raise Exception('文件上传失败, 原因:' % e.message)
        return file_url


if __name__ == '__main__':
    pass
