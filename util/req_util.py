# coding= utf-8
import requests
import json
from config.config import BAIDU_TOKEN_URL, API_KEY, SECRET_KEY


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
            raise e
        return access_token
