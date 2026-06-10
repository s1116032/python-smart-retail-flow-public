import time
import json
import random
from datetime import datetime, timezone
from models.sensor_data import SensorData
from db.redis_client import get_redis_client

# 模擬的設備 ID（例如：一樓入口、二樓入口、出口）
DEVICE_IDS = ["sensor_entrance_01", "sensor_entrance_02", "sensor_exit_01"]
# Redis List 的 Key 名稱
REDIS_KEY = "sensor:hot_data"


def generate_sensor_data() -> dict:
    """隨機產生一筆感測器資料"""
    data = SensorData(
        timestamp=datetime.now(timezone.utc),
        device_id=random.choice(DEVICE_IDS),
        count=random.randint(0, 5),  # 模擬每 0.5 秒偵測到 0~5 人
    )
    # Pydantic V2 的序列化方式，轉成 ISO 8601 格式的字串與 dict
    return data.model_dump(mode="json")


def main():
    redis_client = get_redis_client()
    print("🚀 模擬感測器啟動，開始傳送資料至 Redis...")

    try:
        while True:
            # 1. 產生資料
            sensor_dict = generate_sensor_data()
            json_str = json.dumps(sensor_dict)

            # 2. 寫入 Redis List (LPUSH 寫入左側，O(1) 複雜度)
            redis_client.lpush(REDIS_KEY, json_str)

            # 3. 印出 Log 方便觀察
            print(
                f"📝 寫入 Redis: {sensor_dict['device_id']} | 人數: {sensor_dict['count']}"
            )

            # 4. 暫停 0.5 秒
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 模擬感測器已手動停止。")
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")


if __name__ == "__main__":
    main()
