# 智慧零售客流量感測器 - 熱冷資料分流系統

模擬高併發 IoT 場景，使用 Redis 作為熱資料緩衝層，PostgreSQL 作為冷資料持久化層，實現高效能的時間序列資料寫入架構。

---

## 系統架構

* **Mock Sensor**：每 0.5 秒產生一筆感測器資料，寫入 Redis List (LPUSH)。
* **Redis (Hot Storage)**：作為高併發寫入的緩衝佇列，吸收瞬間流量。
* **Cold Storage Worker**：每 10 秒批次提取 Redis 資料，寫入 PostgreSQL。
* **PostgreSQL (Cold Storage)**：提供 ACID 保證的持久化儲存，並建立時間序列索引。

---

## 啟動方式

1.  **安裝依賴**：
    ```bash
    pip install -r requirements.txt
    ```
2.  **啟動本地 PostgreSQL & Redis**：
    確保服務啟動後，進入 PostgreSQL 並建立此專案所需的資料庫：
    ```sql
    CREATE DATABASE smart_retail;
    ```
3.  **初始化資料庫**：
    ```bash
    python -m scripts.init_db
    ```
4.  **啟動模擬器**：
    ```bash
    python -m scripts.mock_sensor
    ```
5.  **啟動背景 Worker**：
    ```bash
    python -m workers.cold_storage_worker
    ```

## License
Copyright © 2026 hanwu910514.

詳情請參閱[Apache License 2.0](LICENSE)檔案