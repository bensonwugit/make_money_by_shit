#!/usr/bin/env python
"""
Make Money by Shit - Deployment & Production Checklist
生產環境部署檢查清單
"""

import os
import sys
from pathlib import Path

def check_files():
    """檢查所有必要的檔案是否存在"""
    required_files = [
        'run.py',
        'config.py',
        'init_db.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'PROJECT_STRUCTURE.md',
        'app/__init__.py',
        'app/models.py',
        'app/routes.py',
        'app/templates/login.html',
        'app/templates/dashboard.html',
        'app/templates/poop_mode_select.html',
        'app/templates/salary_thief_complete.html',
        'app/templates/normal_mode_complete.html',
        'app/templates/poop_result.html',
        'app/templates/analysis.html',
        'app/templates/settings.html',
        'app/static/css/style.css',
        'app/static/js/main.js',
        'app/static/js/service-worker.js',
        'app/static/manifest.json',
        'Dockerfile',
        'docker-compose.yml',
        '.gitignore',
        '.env.example',
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    return missing_files

def check_dependencies():
    """檢查 Python 依賴"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        print("✅ All required packages installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def main():
    """主檢查函數"""
    print("=" * 60)
    print("Make Money by Shit - Deployment Checklist")
    print("=" * 60)
    print()
    
    # 檢查檔案
    print("📁 Checking files...")
    missing_files = check_files()
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
    
    print()
    
    # 檢查依賴
    print("📦 Checking dependencies...")
    if not check_dependencies():
        print("❌ Run: pip install -r requirements.txt")
        return False
    
    print()
    
    # 生產環境檢查清單
    print("=" * 60)
    print("🚀 PRODUCTION DEPLOYMENT CHECKLIST")
    print("=" * 60)
    print()
    
    checklist = [
        ("🔑 Change SECRET_KEY", "Set unique secret key in .env"),
        ("🔒 Enable HTTPS/SSL", "Use certbot or cloud provider's SSL"),
        ("🗄️ Switch to PostgreSQL", "Update SQLALCHEMY_DATABASE_URI"),
        ("🛡️ Set DEBUG=False", "Disable debug mode in production"),
        ("📧 Configure email", "Setup email for notifications (optional)"),
        ("🔐 Setup database backups", "Automated daily backups"),
        ("📊 Configure monitoring", "Use Sentry or New Relic"),
        ("🔄 Setup CI/CD", "GitHub Actions or similar"),
        ("⚙️ Configure Nginx", "Reverse proxy configuration"),
        ("🐳 Test Docker image", "Build and test Dockerfile"),
        ("🌍 DNS configuration", "Point domain to server"),
        ("📱 Test on mobile", "Verify responsive design"),
        ("♿ Accessibility check", "WCAG 2.1 compliance"),
        ("📝 Legal review", "Review terms & disclaimers"),
        ("🔐 User data protection", "GDPR/Privacy compliance"),
    ]
    
    print("Pre-deployment checks:")
    print()
    for i, (task, details) in enumerate(checklist, 1):
        print(f"{i:2}. {task}")
        print(f"    └─ {details}")
    
    print()
    print("=" * 60)
    print("✅ DEPLOYMENT READY!")
    print("=" * 60)
    print()
    
    print("Quick deployment commands:")
    print()
    print("  Docker:")
    print("    docker build -t mmbs .")
    print("    docker-compose up")
    print()
    print("  Gunicorn:")
    print("    gunicorn -w 4 -b 0.0.0.0:8000 run:app")
    print()
    print("  Development:")
    print("    python run.py")
    print()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
