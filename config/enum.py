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
    UNCHECK = 0  # 未签到
    CHECKED = 1  # 已签到
    FORBID = 2  # 删除


class Open_Check(object):
    """
    当前是否可签到
    """
    YES = 0
    NO = 1


class IS_OPEN(object):
    """
    签到记录是否可查
    """
    YES = 0
    NO = 1
