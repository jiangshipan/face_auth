# coding= utf-8

from flask_limiter import Limiter
from db import app
# 限流器
limiter = Limiter(app=app)
