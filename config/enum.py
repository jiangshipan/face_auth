# coding= utf-8


class UserStatus(object):
    """
    用户状态
    """
    NORMAL = 0
    FORBID = 1


class FaceStatus(object):
    """
    人脸签到状态
    """
    NOCHECK = 0 # 未签到
    CHECKED = 1 # 已签到
    FORBID = 2 # 删除

