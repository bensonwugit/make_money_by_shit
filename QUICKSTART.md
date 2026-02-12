# Quick Start Guide - Make Money by Shit

## 🚀 5分鐘快速開始

### 前置要求
- Python 3.8+
- pip (Python 套件管理器)

### 1️⃣ 克隆/下載專案

```bash
cd make_money_by_shit
```

### 2️⃣ 執行設定腳本

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

或手動設定:

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 初始化資料庫
python init_db.py
```

### 3️⃣ 運行應用

```bash
python run.py
```

### 4️⃣ 打開瀏覽器

訪問: **http://localhost:5000**

## 🔐 預設登入

```
Username: shit
Password: money
```

## 📱 功能概覽

### Dashboard 儀表板
- 最後一次上廁所時間
- 本月賺取金額
- 快速導航

### Make Money - Salary Thief Mode
1. 選擇時間與持續時間
2. 評估氣味 (8 種選擇)
3. 查看賺取金額 & 健康建議

### Make Money - Normal Mode
- 純健康紀錄
- 不追蹤金錢

### Analysis Dashboard
- 腸胃健康評分
- 統計圖表
- 最近紀錄
- 資料匯出

### Settings 設定
- 薪資配置
- 工作時間表
- 深色模式
- 隱私設定

## 🛠️ 故障排除

### Python 未找到
**錯誤:** `python: command not found`
**解決:** 確保 Python 已安裝並加到系統 PATH

### pip 未找到
**錯誤:** `pip: command not found`
**解決:** 嘗試使用 `python -m pip` 或 `python3 -m pip`

### 資料庫錯誤
**錯誤:** `database locked` 或 `database error`
**解決:** 刪除 `make_money_by_shit.db` 文件並重新運行 `python init_db.py`

### 端口已使用
**錯誤:** `Address already in use`
**解決:** 
```bash
# 改變端口
python run.py --port 5001
```

或編輯 `run.py` 中的端口號

## 🌐 部署

### Heroku

1. 建立 `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

2. 推送到 Heroku:
```bash
git push heroku main
```

### 本地網絡訪問

編輯 `run.py`:
```python
app.run(
    host='0.0.0.0',  # 允許外部連接
    port=5000,
    debug=True
)
```

然後訪問: `http://<your-ip>:5000`

## 📊 資料備份

### 導出資料
在 Analysis Dashboard 頁面點擊 "📥 Export Data" 按鈕

### 手動備份資料庫
```bash
# 複製資料庫文件
cp make_money_by_shit.db make_money_by_shit_backup.db
```

## 🔒 生產環境設定

1. 設定環境變數:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-very-secure-key-here
```

2. 使用生產級伺服器:
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 run:app
```

3. 使用 Nginx 作為反向代理

4. 啟用 HTTPS/SSL

## 📞 支援

遇到問題嗎?
- 檢查 README.md
- 查看 GitHub Issues
- 提交 Bug Report

## 📝 授權

MIT License - 詳見 LICENSE 文件

---

**享受你的💩💰之旅！**
