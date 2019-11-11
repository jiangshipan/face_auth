import redis
from config import config
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT)
redis_client = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    # redis_client.set('', '111', ex=1)
    print redis_client.get('1320740751@qq.com')