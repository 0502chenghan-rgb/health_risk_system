# 健康風險評估系統 (Health Risk System)

這是 [填寫你的課程名稱，例如：生活科技與永續] 的期末專案作業。本專案是一個基於 Python Flask 框架開發的網頁系統，結合了決策樹演算法來評估個人的健康風險。

## 🌐 相關連結
* **線上展示網址 (Render):** [貼上你的 Render 連結，例如：https://health-risk-system-40pn.onrender.com]
* **程式碼儲存庫 (GitHub):** https://github.com/0502chenghan-rgb/health_risk_system

## ✨ 主要功能
* **風險評估問卷：** 使用者可以輸入相關健康數據（如身高、體重、生活習慣等）。
* **決策樹預測：** 後端利用決策樹模型（Decision Tree）即時分析並預測健康風險等級。
* **資料庫儲存：** 使用 SQLite (`health.db`) 記錄或管理相關評估數據。

## 📂 檔案結構說明
* `main.py` - 網頁伺服器主程式 (Flask Application)
* `decision_tree.py` - 決策樹演算法與模型邏輯
* `database.py` - 資料庫連線與操作邏輯
* `health.db` - SQLite 資料庫檔案
* `templates/` - 存放前端網頁 HTML 的資料夾
* `requirements.txt` - 雲端部署所需的 Python 套件清單

## 💻 本地端執行方式
若要在本機電腦執行此專案，請依序執行以下指令：

1. 安裝必要套件：
```bash
   pip install -r requirements.txt
