# coding= utf-8
import json
import traceback

from config.enum import FaceStatus, Open_Check
from dao.face_dao import FaceDao
from dao.record_dao import RecordDao
from dao.user_dao import UserDao
from model.face import Face
from config.db import db
from config.config import FACE_LIB_USER_ADD, FACE_SEARCH, FACE_ACCESS
from model.record import Record
from util.face_auth_utils import FaceAuthUtils, Singleton
from util.req_util import RequestUtil
from collections import defaultdict

class FaceService(object):
    """
    人脸服务
    """

    __metaclass__ = Singleton


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
            FaceAuthUtils.save_exception(traceback.format_exc())
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
                    if face.open_check != Open_Check.YES:
                        raise Exception('不在签到时间范围内')
                    if face.status == FaceStatus.CHECKED:
                        raise Exception('已签到')
                    face.status = FaceStatus.CHECKED
                    db.session.commit()
                    return
            raise Exception('人脸验证未通过')
        except Exception as e:
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise Exception(e.message)

    def get_face_by_user_id(self, user_id, filters, page=1):
        """
        根据用户id查询其下人脸信息
        :param
        :return:
        """
        faces, total = FaceDao.get_face_by_user_id(user_id, page, filters)
        if not faces:
            return {'data': [], 'total': 0}
        user = UserDao.get_user_by_user_id(user_id)
        res = {}
        data = []
        for face in faces:
            data.append({
                'id': face.id,
                'name': face.face_name,
                'belong': user.username,
                'url': face.face_url,
                'status': face.status,
                'stu_class': face.face_class
            })
        res.update({
            'data': data,
            'total': total
        })
        return res

    def init_face(self, stu_class, user_id):
        """
        :param stu_class: 班级
        :param user_id: 老师的id
        :return:
        0. 检查现在是否处于签到时期
        1. 统计出未签到的人，生成签到记录
        2. 初始化所有该stu_class & user_id的签到状态为未签到
        3. 修改当前不可进行签到
        """

        # 检查现在是否处于签到时期
        faces = FaceDao.get_by_class_user_id2(stu_class, user_id, Open_Check.YES)
        if not faces:
            raise Exception("暂未开放签到")
        unchecked_faces = FaceDao.get_by_class_user_id(stu_class, user_id, FaceStatus.UNCHECK)
        unchecked = [_.face_name + ' ' for _ in unchecked_faces]
        try:
            record = Record.create(user_id, stu_class, json.dumps({'data': unchecked}))
            RecordDao.insert(record)
            checked_faces = FaceDao.get_by_class_user_id(stu_class, user_id, FaceStatus.CHECKED)
            # 未签到的人不需要初始化了
            for face in checked_faces:
                face.status = FaceStatus.UNCHECK
                face.open_check = Open_Check.NO
            for face in unchecked_faces:
                face.open_check = Open_Check.NO
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise Exception(e.message)


    def get_class_by_user_id(self, user_id):
        faces = FaceDao.get_class_by_user_id(user_id)
        face_class2sum = defaultdict(int)
        res = {'checked': [], 'unchecked': []}
        for face in faces:
            checked = res.get('checked')
            unchecked = res.get('unchecked')
            if face.open_check == Open_Check.YES and face.face_class not in checked:
                checked.append(face.face_class)
            if face.open_check == Open_Check.NO and face.face_class not in unchecked:
                unchecked.append(face.face_class)
            face_class2sum[face.face_class] += 1
        res.update({'sum': face_class2sum})
        return res



    def start_check(self, user_id, stu_class):
        # 检查现在是否处于签到时期
        faces = FaceDao.get_by_class_user_id2(stu_class, user_id, Open_Check.NO)
        if not faces:
            raise Exception("该班已处于签到状态")
        try:
            for face in faces:
                face.open_check = Open_Check.YES
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise Exception(e.message)

    def update_face_status(self, face_id, face_status):
        face = FaceDao.get_face_by_face_id(face_id)
        if not face:
            raise Exception("当前学生信息不存在")
        try:
            face.status = face_status
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            FaceAuthUtils.save_exception(traceback.format_exc())
            raise Exception(e.message)

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
