import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. 建立符合作業規範的 health_logs 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date DATE NOT NULL,
            sleep_hours REAL NOT NULL,
            steps INTEGER NOT NULL,
            mood_score INTEGER NOT NULL,
            risk_level TEXT
        );
    ''')
    
    # 檢查是否已經有資料，避免重複插入
    cursor.execute("SELECT COUNT(*) FROM health_logs")
    if cursor.fetchone()[0] > 0:
        print("資料庫已存在種子資料，跳過初始化。")
        conn.close()
        return

    # 2. 生成具有強烈規律訊號的 90 天種子資料
    start_date = datetime(2026, 3, 20)
    seed_data = []
    
    # 為了確保決策樹能切出完美邊界，我們將資料分成三大組（共 90 天）
    # 高風險組 (23天)：睡眠少、步數少、心情差
    for i in range(23):
        log_date = (start_date + timedelta(days=len(seed_data))).strftime("%Y-%m-%d")
        sleep = round(random.uniform(4.0, 5.3), 1)
        steps = random.randint(1200, 3200)
        mood = random.randint(1, 4)
        seed_data.append((log_date, sleep, steps, mood))
        
    # 正常/普通組 (44天)：數值混合普通
    for i in range(44):
        log_date = (start_date + timedelta(days=len(seed_data))).strftime("%Y-%m-%d")
        sleep = round(random.uniform(6.0, 7.2), 1)
        steps = random.randint(4500, 5800)
        mood = random.randint(5, 6)
        seed_data.append((log_date, sleep, steps, mood))
        
    # 低風險組 (23天)：睡眠足、步數多、心情好
    for i in range(23):
        log_date = (start_date + timedelta(days=len(seed_data))).strftime("%Y-%m-%d")
        sleep = round(random.uniform(7.6, 9.0), 1)
        steps = random.randint(6800, 9800)
        mood = random.randint(7, 10)
        seed_data.append((log_date, sleep, steps, mood))
    
    # 打亂順序，模擬真實每天記錄的情況
    random.shuffle(seed_data)
    
    # 寫入資料庫 (risk_level 保持為空，由決策樹計算)
    cursor.executemany('''
        INSERT INTO health_logs (log_date, sleep_hours, steps, mood_score, risk_level)
        VALUES (?, ?, ?, ?, NULL)
    ''', seed_data)
    
    conn.commit()
    conn.close()
    print(f"成功建立資料庫 '{DB_NAME}' 並匯入 90 天的高品質種子資料！")

if __name__ == "__main__":
    init_db()