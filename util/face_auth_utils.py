# coding= utf-8
import random
import base64
import requests

from config.config import FILE_PATH


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
    def image2base64(image_url):
        """
        图片base64编码
        :param image_url:
        :return:
        """
        with open(image_url, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data


if __name__ == '__main__':
    face_url = '/Users/jiangshipan/Desktop/IMG_0040.JPG'
    FaceAuthUtils.image2base64(face_url)
