from db.postgres_client import get_pg_connection

def init_database():
    conn = None
    try:
        conn = get_pg_connection()
        cursor = conn.cursor()
        
        # 建立感測器日誌資料表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            device_id VARCHAR(50) NOT NULL,
            count INTEGER NOT NULL
        );
        """
        cursor.execute(create_table_query)
        
        # 面試亮點：針對時間序列資料建立 Index，加速未來查詢特定時間區間的效能
        create_index_query = """
        CREATE INDEX IF NOT EXISTS idx_sensor_logs_timestamp 
        ON sensor_logs (timestamp);
        """
        cursor.execute(create_index_query)
        
        # 面試亮點：複合索引，針對特定設備在特定時間的查詢
        create_device_index_query = """
        CREATE INDEX IF NOT EXISTS idx_sensor_logs_device_time 
        ON sensor_logs (device_id, timestamp);
        """
        cursor.execute(create_device_index_query)
        
        conn.commit()
        print("✅ PostgreSQL 資料表與索引初始化成功！")
        
    except Exception as e:
        print(f"❌ 初始化失敗: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()