import psycopg2
from config.settings import PG_HOST, PG_PORT, PG_DBNAME, PG_USER, PG_PASSWORD

def get_pg_connection():
    """取得 PostgreSQL 連線"""
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD
    )
    return conn