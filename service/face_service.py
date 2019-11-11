# coding= utf-8
import json
from dao.face_dao import FaceDao
from model.face import Face
from config.db import db
from config.config import FACE_LIB_USER_ADD, FACE_SEARCH, FACE_ACCESS
from util.face_auth_utils import FaceAuthUtils
from util.req_util import RequestUtil
from config.log import logger


class FaceService(object):
    """
    人脸服务
    """

    def face_add(self, face_info, file_base64, face_url):
        """
        添加人脸到人脸库
        :return:
        """
        user_id = face_info.get('user_id')
        face_name = face_info.get('face_name')
        face_url = 'http://www.wvue.com.cn/jsp_download/11566976362_.pic.jpg'
        face = FaceDao.get_by_user_id_and_face_name(user_id, face_name)
        if face:
            raise Exception('face is exist')
        face = Face.create(user_id, face_name, face_url)
        try:
            FaceDao.insert(face)
            params = {'image': file_base64, 'image_type': 'BASE64', 'group_id': user_id, 'user_id': face.id
                , 'quality_control': 'NORMAL'}
            access_token = RequestUtil.get_access_token()
            url = FACE_LIB_USER_ADD + "?access_token=" + str(access_token)
            resp = RequestUtil.send_post(url=url, params=json.dumps(params),
                                         headers={'content-type': 'application/json'})
            self.check_response(resp)
            db.session.commit()
        except Exception as e:
            logger.error(e.message)
            db.session.rollback()
            raise Exception(e.message)

    def face_search(self, face_info, file_base64):
        """
        指定用户组中搜索人像
        :param face_info:
        :return:
        """
        user_id = face_info.get('user_id')
        try:
            params = {'image': file_base64, 'image_type': 'BASE64', 'group_id_list': str(user_id),
                      'quality_control': 'NORMAL',
                      'liveness_control': 'NORMAL'}
            access_token = RequestUtil.get_access_token()
            url = FACE_SEARCH + "?access_token=" + str(access_token)
            resp = RequestUtil.send_post(url=url, params=json.dumps(params),
                                         headers={'content-type': 'application/json'})
            self.check_response(resp)
            result = resp.json().get('result')
            for res in result.get('user_list'):
                if res.get('score') > FACE_ACCESS:
                    return
            raise Exception('人脸验证未通过')
        except Exception as e:
            logger.error(e.message)
            raise Exception(e.message)

    def get_face_by_user_ids(self, info):
        """
        根据用户ids查询人脸信息
        :param user_ids:
        :return:
        """
        user_ids = info.get('user_ids')
        page = info.get('page')
        print user_ids, page
        faces = FaceDao.get_face_by_user_ids(user_ids, page)
        if not faces:
            return []
        res = []
        for face in faces:
            res.append({
                'id': face.id,
                'name': face.face_name,
                'belong': face.user_id,
                'url': face.face_url
            })
        return res


    def check_response(self, resp):
        """
        检验baidu_api的response
        :param resp:
        :return:
        """
        error_code = resp.json().get('error_code')
        error_msg = resp.json().get('error_msg')
        if not resp or error_code != 0:
            raise Exception(error_msg)
