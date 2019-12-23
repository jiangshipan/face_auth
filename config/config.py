# coding= utf-8

# redis配置
REDIS_HOST = '119.3.212.165'
REDIS_PORT = '6379'
# mysql配置
DATABASE_URI = 'mysql+pymysql://jiangshipan:19980502@119.3.212.165:3306/face_auth?charset=utf8mb4'


# 邮件配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = '1320740751@qq.com'
MAIL_PASSWORD = 'gdlgnjyvifnoibib'

# 分页信息
PAGE_LIMIT = 10
# 允许上传的文件类型
FILE_EXT = ['png', 'jpeg', 'jpg', 'JPG', 'PNG', 'JPEG']
# macos
# FILE_PATH = '/Users/jiangshipan/Desktop/upload_img/'
# linux服务器
FILE_PATH = '/data/nginx/html/images/'
# 随机文件夹
FILE_DIR = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9']
# 日志文件
# mac
# LOG_NAME = '/Users/jiangshipan/Desktop/today_log'
LOG_NAME = '/data/nginx/log/today_log'


# 获取access_token
BAIDU_TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
API_KEY = 'Uz50PwtKOd2LNWKATA3zMLyi'
SECRET_KEY = 'seMvUxWPqFYWKhCgGk0e9GoSqw9D9lI6'

# 人脸库相关URL
FACE_LIB_USER_ADD = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add'  # 人脸库管理-人脸注册
FACE_LIB_USER_UPDATE = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update'  # 人脸库管理-人脸更新
FACE_LIB_USER_DELETE = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update'  # 人脸库管理-删除用户
FACE_LIB_UER_GET = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get'  # 人脸库管理-用户信息查询
FACE_LIB_USER_COPY = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/copy'  # 人脸库管理-复制用户
FACE_LIB_GROUP_LIST = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist'  # 人脸库管理-获取组列表
FACE_LIB_GROUP_USER_LIST = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers'  # 人脸库管理-获取用户列表
FACE_LIB_USER_GETS = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist'  # 人脸库管理-获取用户人脸列表
FACE_LIB_GROUP_ADD = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add'  # 人脸库管理-创建用户组
FACE_LIB_GROUP_DELETE = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete'  # 人脸库管理-删除用户组
FACE_LIB_DELETE_FACE = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete'  # 人脸库管理-删除人脸
# 人脸搜索
FACE_SEARCH = 'https://aip.baidubce.com/rest/2.0/face/v3/search'


# 人脸相似评分
FACE_ACCESS = 80

#人脸检测/录入 url
FACE_FRONT = 'http://localhost:8080/'