import redis
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

# 建立全域的 Redis 連線池與客戶端
redis_pool = redis.ConnectionPool(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=REDIS_DB, 
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)

def get_redis_client() -> redis.Redis:
    return redis_client