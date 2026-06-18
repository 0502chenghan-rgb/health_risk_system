from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from decision_tree import classify_health_risk

app = FastAPI(title="智慧健康日誌與風險評估系統")

# 設置 HTML 模板目錄
templates = Jinja2Templates(directory="templates")
DB_NAME = "health.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱取值
    return conn

# ==========================================
# 1. 前端網頁路由：渲染主介面 (已修正新版 FastAPI 語法變更)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 這裡使用了新版 FastAPI 最安全的關鍵字參數寫法，避免 unhashable type 錯誤
    return templates.TemplateResponse(request=request, name="index.html")

# ==========================================
# 2. 符合作業規範的標準 RESTful API 端點
# ==========================================

# [GET] 取得所有健康日誌紀錄
@app.get("/health-logs")
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_logs ORDER BY log_date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        log = dict(row)
        # 如果資料庫內 risk_level 為空，則當場用決策樹幫它計算補上
        if not log["risk_level"]:
            log["risk_level"] = classify_health_risk(log["sleep_hours"], log["steps"], log["mood_score"])
        logs.append(log)
    return logs

# [POST] 新增一筆健康日誌 (送出時即由決策樹分類並寫入 risk_level)
@app.post("/health-logs")
def create_log(log_date: str = Form(...), sleep_hours: float = Form(...), steps: int = Form(...), mood_score: int = Form(...)):
    # 核心整合：將決策樹模型嵌入商務邏輯
    risk = classify_health_risk(sleep_hours, steps, mood_score)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO health_logs (log_date, sleep_hours, steps, mood_score, risk_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (log_date, sleep_hours, steps, mood_score, risk))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"資料庫寫入失敗: {str(e)}")
    conn.close()
    return {"status": "success", "risk_level": risk}

# [PUT] 修改指定日誌
@app.put("/health-logs/{log_id}")
def update_log(log_id: int, log_date: str, sleep_hours: float, steps: int, mood_score: int):
    risk = classify_health_risk(sleep_hours, steps, mood_score)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE health_logs 
        SET log_date = ?, sleep_hours = ?, steps = ?, mood_score = ?, risk_level = ?
        WHERE id = ?
    ''', (log_date, sleep_hours, steps, mood_score, risk, log_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

# [DELETE] 刪除指定日誌
@app.delete("/health-logs/{log_id}")
def delete_log(log_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM health_logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()
    return {"status": "success"}

# [GET] 依決策樹邏輯「即時」計算並回傳風險等級
@app.get("/health-logs/risk")
def get_live_risk(sleep: float, steps: int, mood: int):
    risk = classify_health_risk(sleep, steps, mood)
    return {"risk_level": risk}