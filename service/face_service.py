# coding= utf-8
import json

from config.enum import FaceStatus
from dao.face_dao import FaceDao
from model.face import Face
from config.db import db
from config.config import FACE_LIB_USER_ADD, FACE_SEARCH, FACE_ACCESS
from util.face_auth_utils import FaceAuthUtils
from util.req_util import RequestUtil

class FaceService(object):
    """
    人脸服务
    """

    def face_add(self, face_info):
        """
        添加人脸到人脸库
        :return:
        """
        user_id = face_info.get('user_id')
        face_name = face_info.get('face_name')
        face_class = face_info.get('face_class')
        base64_code = face_info.get('base64_code')
        face = FaceDao.get_by_user_id_and_face_name(user_id, face_name)
        if face:
            raise Exception('face is exist')
        try:
            # 上传图片
            face_url = FaceAuthUtils.base642imag(base64_code)
            face = Face.create(user_id, face_name, face_url, face_class)
            FaceDao.insert(face)
            params = {'image': base64_code, 'image_type': 'BASE64', 'group_id': user_id, 'user_id': face.id
                , 'quality_control': 'NORMAL'}
            access_token = RequestUtil.get_access_token()
            url = FACE_LIB_USER_ADD + "?access_token=" + str(access_token)
            resp = RequestUtil.send_post(url=url, params=json.dumps(params),
                                         headers={'content-type': 'application/json'})
            self.check_response(resp)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e.message)

    def face_search(self, face_info):
        """
        指定用户组中搜索人像
        user_id = 教师id = group_id
        百度返回 user_id = face_id
        :param face_info:
        :return:
        """
        try:
            user_id = face_info.get('user_id')
            base64_code = face_info.get('base64_code')
            params = {'image': base64_code, 'image_type': 'BASE64', 'group_id_list': str(user_id),
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
                    face_id = res.get('user_id')
                    face = FaceDao.get_face_by_face_id(face_id)
                    if not face:
                        raise Exception('不存在该学生')
                    if face.open_check != 0:
                        raise Exception('不在签到时间范围内')
                    if face.status == FaceStatus.CHECKED:
                        raise Exception('已签到')
                    face.status = FaceStatus.CHECKED
                    db.session.commit()
                    return
            raise Exception('人脸验证未通过')
        except Exception as e:
            raise Exception(e.message)

    def get_face_by_user_id(self, user_id, page=1):
        """
        根据用户id查询其下人脸信息
        :param
        :return:
        """
        face = FaceDao.get_face_by_user_id(user_id, page)
        if not face:
            return []
        res = {
            'id': face.id,
            'name': face.face_name,
            'belong': face.user_id,
            'url': face.face_url,
            'status': face.status,
            'stu_class': face.face_class
        }
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
