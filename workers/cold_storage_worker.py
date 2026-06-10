import time
import json
import psycopg2.extras
from db.redis_client import get_redis_client
from db.postgres_client import get_pg_connection
from config.settings import REDIS_HOST, REDIS_PORT

REDIS_KEY = "sensor:hot_data"
BATCH_SIZE = 100  # 每次最多從 Redis 取出的筆數
SLEEP_INTERVAL = 10  # 每 10 秒執行一次搬遷


def transfer_data_to_postgres():
    redis_client = get_redis_client()

    # 1. 查看目前 Redis 裡有多少資料
    list_len = redis_client.llen(REDIS_KEY)
    if list_len == 0:
        print("⏳ Redis 無新資料，等待中...")
        return

    print(f"🔥 發現 {list_len} 筆熱資料，準備搬遷...")

    # 2. 使用 LRANGE 取出最舊的 BATCH_SIZE 筆資料 (從 List 右側取出)
    # 注意：LRANGE -100 -1 代表取倒數 100 筆到倒數第 1 筆
    start_index = -BATCH_SIZE
    raw_data_list = redis_client.lrange(REDIS_KEY, start_index, -1)

    if not raw_data_list:
        return

    # 3. 解析資料並準備批次寫入
    pg_data = []
    for json_str in raw_data_list:
        data = json.loads(json_str)
        # 轉成 Tuple，對應 SQL 的 (timestamp, device_id, count)
        pg_data.append((data["timestamp"], data["device_id"], data["count"]))

    conn = None
    try:
        conn = get_pg_connection()
        cursor = conn.cursor()

        # 4. 面試亮點：使用 execute_values 進行 Batch Insert，大幅降低 DB I/O
        insert_query = """
            INSERT INTO sensor_logs (timestamp, device_id, count) 
            VALUES %s;
        """
        psycopg2.extras.execute_values(cursor, insert_query, pg_data)

        # 5. 確保 PG 寫入成功後，再刪除 Redis 的資料 (資料一致性保證)
        # 面試亮點：LTRIM 保留 List 前面的資料（比較新的資料），刪除已經寫入 PG 的舊資料
        # 保留從 0 到 -(BATCH_SIZE + 1) 的資料，等同於刪除最後 BATCH_SIZE 筆
        redis_client.ltrim(REDIS_KEY, 0, -(BATCH_SIZE + 1))

        # 6. 提交 PG Transaction
        conn.commit()
        print(f"✅ 成功將 {len(pg_data)} 筆資料寫入 PostgreSQL，並已清除 Redis 緩存。")

    except Exception as e:
        print(f"❌ 搬遷失敗，進行 Rollback: {e}")
        if conn:
            conn.rollback()
        # 重要：如果 PG 寫入失敗，我們「不會」刪除 Redis 的資料，下個循環會再嘗試
    finally:
        if conn:
            conn.close()


def main():
    print("🛠️ 冷資料搬遷 Worker 啟動...")
    # 確認 Redis 連線
    try:
        redis_client = get_redis_client()
        redis_client.ping()
    except Exception as e:
        print(f"❌ 無法連線至 Redis，Worker 停止: {e}")
        return

    try:
        while True:
            transfer_data_to_postgres()
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 冷資料搬遷 Worker 已手動停止。")


if __name__ == "__main__":
    main()
