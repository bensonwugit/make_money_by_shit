# Make Money by Shit - 完整專案結構

```
make_money_by_shit/
│
├── 📄 根目錄檔案
│   ├── run.py                      # 應用入口 & 開發伺服器
│   ├── init_db.py                 # 資料庫初始化
│   ├── config.py                  # Flask 配置
│   ├── requirements.txt            # Python 依賴
│   ├── .env.example               # 環境變數範本
│   ├── .gitignore                 # Git 忽略規則
│   │
│   ├── 📚 文檔
│   ├── README.md                  # 完整說明文檔
│   ├── QUICKSTART.md              # 快速開始指南
│   ├── PROJECT_STRUCTURE.md       # 這個檔案
│   │
│   ├── 🐳 Docker
│   ├── Dockerfile                 # Docker 鏡像定義
│   ├── docker-compose.yml         # Docker Compose 配置
│   ├── .dockerignore              # Docker 忽略規則
│   │
│   └── 🔧 設定腳本
│       ├── setup.sh               # Linux/Mac 設定腳本
│       └── setup.bat              # Windows 設定腳本
│
├── 📁 app/                         # 主應用程式目錄
│   ├── __init__.py                # Flask 應用工廠
│   ├── models.py                  # 資料庫模型 (ORM)
│   ├── routes.py                  # 所有路由定義
│   │
│   ├── 📁 templates/              # Jinja2 HTML 模板
│   │   ├── login.html             # 登入頁面
│   │   ├── navbar.html            # 導覽列組件
│   │   ├── footer.html            # 頁尾組件
│   │   │
│   │   ├── 🏠 儀表板 (Dashboard)
│   │   ├── dashboard.html         # 主儀表板頁面
│   │   │
│   │   ├── 💩 大便記錄 (Poop Recording)
│   │   ├── poop_mode_select.html  # 模式選擇 (Salary Thief vs Normal)
│   │   ├── salary_thief_complete.html    # Salary Thief 完整表單
│   │   ├── salary_thief_step1.html       # 舊: Salary Thief 第1步 (不用)
│   │   ├── salary_thief_step2.html       # 舊: Salary Thief 第2步 (不用)
│   │   ├── normal_mode_complete.html     # Normal Mode 完整表單
│   │   ├── normal_mode_step1.html        # 舊: Normal Mode 第1步 (不用)
│   │   ├── poop_result.html      # 結果頁面 (金錢 & 建議)
│   │   │
│   │   ├── 📊 分析 (Analysis)
│   │   ├── analysis.html          # 分析儀表板 (圖表 & 統計)
│   │   │
│   │   ├── ⚙️ 設定 (Settings)
│   │   ├── settings.html          # 設定頁面
│   │   │
│   │   └── 📱 PWA
│   │       └── pwa.html           # PWA 進入點
│   │
│   ├── 📁 static/                 # 靜態資源
│   │   ├── 🎨 css/
│   │   │   └── style.css          # 主樣式表 (Mobile First)
│   │   │
│   │   ├── 💻 js/
│   │   │   ├── main.js            # 全域 JavaScript & 工具函數
│   │   │   └── service-worker.js  # PWA Service Worker
│   │   │
│   │   ├── 🖼️ images/            # 圖片資源目錄
│   │   └── 📋 manifest.json       # PWA Manifest
│
├── 📦 venv/                       # Python 虛擬環境 (本地開發)
│
└── 🗄️ make_money_by_shit.db       # SQLite 資料庫 (執行時建立)
```

## 📋 核心元件詳解

### 後端 (Python Flask)

#### models.py - 資料模型
```
User
├── id, username, password_hash
├── salary_amount, salary_currency
├── salary_type (monthly/hourly)
├── working_days_per_week, working_hours_per_day
├── 設定: language, country, dark_mode, privacy_mode
└── 關係: poop_records[], achievements[]

PoopRecord
├── id, user_id (FK), datetime
├── duration_minutes, mode ('salary_thief'/'normal')
├── smell_condition (8 種類型)
├── money_earned
└── 方法: calculate_money(), get_health_suggestion()

Achievement
├── id, user_id (FK), achievement_type
├── achieved_at
└── 方法: get_title(), get_description()
```

#### routes.py - API 路由
```
認證 (auth_bp)
├── POST /auth/login       登入
└── GET/POST /auth/logout  登出

儀表板 (dashboard_bp)
└── GET /                  主頁面

大便紀錄 (poop_bp)
├── GET /poop/mode-select      選擇模式
├── GET/POST /poop/salary-thief    Salary Thief Mode
├── GET/POST /poop/normal           Normal Mode
└── GET /poop/result/<id>      結果頁面

分析 (analysis_bp)
├── GET /analysis/dashboard     分析儀表板
└── GET /analysis/export        匯出資料 (JSON)

設定 (settings_bp)
├── GET /settings/              設定頁面
└── POST /settings/update       更新設定
```

### 前端 (HTML/CSS/JavaScript)

#### 樣式結構 (style.css)
```
CSS 變數 (CSS Variables)
├── 顏色主題: primary, secondary, success, danger
├── 背景色: bg-primary, bg-secondary
├── 間距: spacing-xs to spacing-xl
├── 圓角: radius-sm to radius-full

深色模式支援
└── [data-dark-mode="true"] 選擇器

元件類別
├── .btn, .btn-primary, .btn-large
├── .form-group, .alert
├── .card, .stat-card
├── .modal, .modal-content
├── .smell-option, .smell-options
└── 響應式: @media (max-width: 768px)

動畫
├── @keyframes bounce (登入頁面)
├── @keyframes slideIn (通知)
└── @keyframes fadeIn (步驟表單)
```

#### JavaScript 功能 (main.js)
```
工具函數
├── formatCurrency()       格式化金錢
├── formatDateTime()       格式化日期
├── getTimeAgo()           計算時間差 (人類易讀)
├── showToast()            顯示通知
├── toggleDarkMode()       深色模式開關
└── apiRequest()           API 請求助手

初始化
├── loadDarkModePreference()   載入深色模式偏好
├── initTooltips()             初始化提示
└── DOMContentLoaded 事件

全域狀態
└── hasUnsavedChanges      追蹤未保存的更改
```

#### Service Worker (service-worker.js)
```
快取策略
├── 安裝事件: 快取靜態資源
├── 啟動事件: 清理舊快取
└── 擷取事件: Cache First + Network Fallback

離線支援
└── 離線時使用快取
```

## 🔄 頁面流程

### 使用者旅程

1. **登入**
   - /auth/login → 輸入 shit / money
   - 建立 Session (7 天)

2. **Dashboard**
   - / → 顯示最後紀錄、本月收入、快速卡片

3. **選擇模式**
   - /poop/mode-select → Salary Thief vs Normal

4. **Salary Thief Mode**
   - /poop/salary-thief (GET)
   - 填表: 時間 + 持續時間 + 氣味
   - 計算: money_earned = duration × salary_per_minute
   - /poop/result/123 → 顯示結果

5. **Normal Mode**
   - /poop/normal (GET)
   - 填表: 時間 + 持續時間 + 氣味
   - /poop/result/456 → 顯示結果 (無金錢)

6. **分析**
   - /analysis/dashboard → 健康評分、圖表
   - /analysis/export → 匯出 JSON

7. **設定**
   - /settings/ → 編輯薪資、工作時間、偏好
   - /auth/logout → 登出

## 🗄️ 資料庫架構

### SQLite (開發環境)

```sql
-- Users 表
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(255),
    created_at DATETIME,
    salary_amount FLOAT,
    salary_currency VARCHAR(3),
    salary_type VARCHAR(10),
    working_days_per_week INTEGER,
    working_hours_per_day INTEGER,
    language VARCHAR(5),
    country VARCHAR(64),
    dark_mode BOOLEAN,
    poop_reminder_enabled BOOLEAN,
    privacy_mode_enabled BOOLEAN
);

-- Poop Records 表
CREATE TABLE poop_record (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FK,
    datetime DATETIME,
    duration_minutes INTEGER,
    mode VARCHAR(20),
    smell_condition VARCHAR(50),
    money_earned FLOAT,
    created_at DATETIME
);

-- Achievements 表
CREATE TABLE achievement (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FK,
    achievement_type VARCHAR(50),
    achieved_at DATETIME
);
```

## 🚀 部署選項

### 本地開發
```bash
python run.py
```

### Docker
```bash
docker-compose up
```

### 生產環境 (Gunicorn + Nginx)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Heroku
```bash
git push heroku main
```

### AWS/Azure/GCP
使用相應的部署服務

## 🔐 安全特性

- ✅ 密碼雜湊 (Werkzeug)
- ✅ Session 安全 (HttpOnly, SameSite)
- ✅ CSRF 保護 (Flask-WTF)
- ✅ SQL 注入防護 (SQLAlchemy ORM)
- ✅ 使用者認證 (Flask-Login)
- ✅ 隱私模式 (隱藏金額)

## 📊 API 回應格式

### 成功回應
```json
{
    "status": "success",
    "record_id": 123,
    "money_earned": 50.25,
    "suggestion": "Great digestion! Keep up the good work."
}
```

### 錯誤回應
```json
{
    "status": "error",
    "message": "Invalid input"
}
```

## 🎨 設計系統

### 顏色方案
- **主要**: #FFB347 (橙色)
- **次要**: #FF6B9D (粉色)
- **成功**: #52C41A (綠色)
- **危險**: #FF4D4F (紅色)

### 間距 (8px 基線)
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

### 斷點
- 小屏: < 480px
- 平板: 768px - 1024px
- 桌面: > 1024px

## 📝 開發規約

### 命名慣例
- Python: snake_case (models, routes)
- JavaScript: camelCase (functions)
- CSS: kebab-case (classes)
- HTML: kebab-case (data attributes)

### 檔案組織
- 模型層: models.py
- 視圖層: routes.py + templates/
- 靜態資源: static/

### 提交訊息
```
feat: 新增功能描述
fix: 修復 Bug
docs: 文檔更新
style: 代碼格式
refactor: 程式碼重構
```

---

**上線日期**: 2026-02-11
**版本**: 1.0.0
**授權**: MIT
