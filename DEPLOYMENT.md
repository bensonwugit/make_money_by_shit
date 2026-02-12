# Deployment Guide - Make Money by Shit

## 🚀 部署指南

### 前置條件
- Python 3.8+
- PostgreSQL (推薦生產環境)
- Docker & Docker Compose (可選)
- Nginx 或其他反向代理
- SSL 證書 (HTTPS)

---

## 📋 部署步驟

### 1️⃣ 環境準備

#### 克隆專案
```bash
git clone https://github.com/yourusername/make-money-by-shit.git
cd make_money_by_shit
```

#### 建立 .env 檔案
```bash
cp .env.example .env
```

編輯 `.env`:
```env
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=your-super-secure-random-key-min-32-chars
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/make_money_by_shit
```

#### 生成 SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2️⃣ 資料庫設定

#### 使用 PostgreSQL (推薦)

安裝 PostgreSQL:
```bash
# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

建立資料庫:
```bash
sudo -u postgres createdb make_money_by_shit
sudo -u postgres createuser mmbs_user
```

設定連接字串:
```env
DATABASE_URL=postgresql://mmbs_user:password@localhost/make_money_by_shit
```

更新 `config.py`:
```python
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

初始化資料庫:
```bash
python init_db.py
```

### 3️⃣ 應用設定

#### 安裝依賴
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
pip install gunicorn  # 生產伺服器
```

#### 收集靜態文件
```bash
# 如果使用 Nginx
python -m flask collect-static
```

### 4️⃣ Systemd 服務配置 (Linux)

建立 `/etc/systemd/system/mmbs.service`:

```ini
[Unit]
Description=Make Money by Shit
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/make_money_by_shit
Environment="PATH=/var/www/make_money_by_shit/venv/bin"
ExecStart=/var/www/make_money_by_shit/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8000 \
    -m 0007 \
    run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

啟動服務:
```bash
sudo systemctl daemon-reload
sudo systemctl start mmbs
sudo systemctl enable mmbs
```

檢查狀態:
```bash
sudo systemctl status mmbs
journalctl -u mmbs -f
```

### 5️⃣ Nginx 反向代理配置

建立 `/etc/nginx/sites-available/make-money-by-shit`:

```nginx
upstream mmbs_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 20M;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 證書 (使用 Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 安全頭
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # 靜態文件
    location /static/ {
        alias /var/www/make_money_by_shit/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 代理到應用
    location / {
        proxy_pass http://mmbs_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

啟用網站:
```bash
sudo ln -s /etc/nginx/sites-available/make-money-by-shit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6️⃣ SSL 證書設定 (Let's Encrypt)

安裝 Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

取得證書:
```bash
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

自動更新:
```bash
sudo certbot renew --quiet
# 添加到 crontab
sudo crontab -e
# 添加: 0 0 * * * certbot renew --quiet
```

### 7️⃣ Docker 部署

#### 構建鏡像
```bash
docker build -t mmbs:latest .
```

#### 運行容器
```bash
docker-compose up -d
```

#### 查看日誌
```bash
docker-compose logs -f web
```

#### 停止容器
```bash
docker-compose down
```

### 8️⃣ 監控和維護

#### 日誌查看
```bash
# Systemd
journalctl -u mmbs -n 100

# Docker
docker-compose logs -f
```

#### 資料庫備份
```bash
# PostgreSQL
pg_dump make_money_by_shit > backup_$(date +%Y%m%d).sql

# 自動每日備份
0 2 * * * pg_dump make_money_by_shit > /backups/mmbs_$(date +\%Y\%m\%d).sql
```

#### 備份恢復
```bash
psql make_money_by_shit < backup_20260211.sql
```

#### 效能監控
```bash
# 使用 Sentry for error tracking
pip install sentry-sdk

# 在 __init__.py 中:
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

---

## 🔒 安全檢查清單

- [ ] 變更預設密碼
- [ ] 設定強 SECRET_KEY
- [ ] 啟用 HTTPS/SSL
- [ ] 配置 Firewall
  ```bash
  sudo ufw enable
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  ```
- [ ] 限制 SSH 訪問
- [ ] 設定 fail2ban 防止暴力攻擊
  ```bash
  sudo apt-get install fail2ban
  ```
- [ ] 啟用 2FA (如適用)
- [ ] 定期更新系統和依賴
  ```bash
  sudo apt-get update && sudo apt-get upgrade
  pip install --upgrade pip
  pip install --upgrade -r requirements.txt
  ```
- [ ] 定期備份資料庫
- [ ] 監控服務器資源 (CPU, Memory, Disk)

---

## 📊 效能優化

### 快取設定
```python
# config.py
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
```

### 資料庫優化
```python
# 添加索引
db.Index('idx_user_id', PoopRecord.user_id)
db.Index('idx_datetime', PoopRecord.datetime)
```

### CDN 配置
推薦使用 CloudFront 或 Cloudflare 加速靜態資源

### 壓縮
```nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

---

## 🚨 故障排除

### 503 Service Unavailable
```bash
# 檢查 Gunicorn 狀態
sudo systemctl status mmbs

# 查看日誌
journalctl -u mmbs -n 50

# 重啟服務
sudo systemctl restart mmbs
```

### 資料庫連接失敗
```bash
# 檢查 PostgreSQL
sudo systemctl status postgresql

# 測試連接
psql -U mmbs_user -d make_money_by_shit -h localhost
```

### 靜態文件 404
```bash
# 確認路徑
ls -la /var/www/make_money_by_shit/app/static/

# 檢查權限
sudo chown -R www-data:www-data /var/www/make_money_by_shit
```

### SSL 證書過期
```bash
# 檢查有效期
sudo certbot certificates

# 強制更新
sudo certbot renew --force-renewal
```

---

## 📈 升級流程

### 更新應用

```bash
# 停止服務
sudo systemctl stop mmbs

# 備份資料庫
pg_dump make_money_by_shit > backup_pre_upgrade.sql

# 拉取最新代碼
git pull origin main

# 安裝新依賴
source venv/bin/activate
pip install -r requirements.txt

# 運行遷移 (如有)
python manage.py db upgrade

# 重啟服務
sudo systemctl start mmbs

# 驗証
curl https://your-domain.com/
```

---

## 📞 支援和資源

- [Flask 文檔](https://flask.palletsprojects.com/)
- [PostgreSQL 文檔](https://www.postgresql.org/docs/)
- [Nginx 文檔](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Systemd 文檔](https://www.freedesktop.org/software/systemd/man/)

---

**最後更新**: 2026-02-11
**版本**: 1.0.0
