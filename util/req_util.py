# coding= utf-8
import requests
import json
import traceback
from config.config import BAIDU_TOKEN_URL, API_KEY, SECRET_KEY
from util.face_auth_utils import FaceAuthUtils


class RequestUtil(object):

    @staticmethod
    def send_post(url, params, headers):
        """
        发送post请求
        :param url:
        :param params:
        :param headers:
        :return:
        """
        resp = requests.post(url=url, data=params, headers=headers)
        return resp

    @staticmethod
    def get_access_token():
        """
        获取access_token
        :return:
        """
        url = BAIDU_TOKEN_URL + '?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
        try:
            resp = requests.get(url=url).text
            access_token = json.loads(resp).get('access_token')
        except Exception as e:
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise e
        return access_token

if __name__ == '__main__':
    print RequestUtil.get_access_token()
