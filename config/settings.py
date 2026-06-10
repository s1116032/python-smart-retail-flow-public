import os
from dotenv import load_dotenv

load_dotenv()

# Redis 設定
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# PostgreSQL 設定
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DBNAME = os.getenv("PG_DBNAME", "smart_retail")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")