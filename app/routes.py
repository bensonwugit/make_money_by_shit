from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, PoopRecord, Achievement
from datetime import datetime, timedelta
import json

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')
poop_bp = Blueprint('poop', __name__, url_prefix='/poop')
analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

# ======================== AUTH ROUTES ========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            login_user(user, remember=True)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# ======================== DASHBOARD ROUTES ========================
@dashboard_bp.route('/')
def index():
    """Main dashboard"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Get last poop record
    last_record = PoopRecord.query.filter_by(user_id=current_user.id).order_by(PoopRecord.datetime.desc()).first()
    
    # Get money earned this month
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    monthly_records = PoopRecord.query.filter(
        PoopRecord.user_id == current_user.id,
        PoopRecord.datetime >= month_start,
        PoopRecord.mode == 'salary_thief'
    ).all()
    monthly_earnings = sum(r.money_earned for r in monthly_records)
    
    # Get total records
    total_records = PoopRecord.query.filter_by(user_id=current_user.id).count()
    
    # Calculate salary per minute
    salary_per_minute = current_user.get_salary_per_minute()
    
    # Format last record time
    last_record_time = ""
    if last_record:
        delta = datetime.utcnow() - last_record.datetime
        if delta.total_seconds() < 60:
            last_record_time = "Just now"
        elif delta.total_seconds() < 3600:
            minutes = int(delta.total_seconds() / 60)
            last_record_time = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif delta.total_seconds() < 86400:
            hours = int(delta.total_seconds() / 3600)
            last_record_time = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = int(delta.total_seconds() / 86400)
            last_record_time = f"{days} day{'s' if days > 1 else ''} ago"
    
    # Greeting message
    greeting_message = f"Welcome back, {current_user.username}! 👋"
    
    return render_template('dashboard.html', 
                         last_record_time=last_record_time,
                         monthly_earnings=monthly_earnings,
                         total_records=total_records,
                         user_salary=current_user.salary_amount,
                         user_currency=current_user.salary_currency,
                         salary_per_minute=salary_per_minute,
                         greeting_message=greeting_message,
                         user_dark_mode=current_user.dark_mode)

# ======================== POOP ROUTES ========================
@poop_bp.route('/mode-select', methods=['GET'])
@login_required
def mode_select():
    """Select poop mode"""
    return render_template('poop_mode_select.html')

@poop_bp.route('/salary-thief', methods=['GET', 'POST'])
@login_required
def salary_thief():
    """Salary Thief Mode"""
    if request.method == 'POST':
        data = request.get_json()
        datetime_str = data.get('datetime')
        duration = int(data.get('duration'))
        smell = data.get('smell')
        
        try:
            poop_datetime = datetime.fromisoformat(datetime_str)
        except:
            poop_datetime = datetime.utcnow()
        
        # Create record
        record = PoopRecord(
            user_id=current_user.id,
            datetime=poop_datetime,
            duration_minutes=duration,
            mode='salary_thief',
            smell_condition=smell
        )
        record.calculate_money(user=current_user)
        
        db.session.add(record)
        db.session.commit()
        
        # Check achievements
        check_achievements(current_user.id)
        
        return jsonify({
            'status': 'success',
            'record_id': record.id,
            'money_earned': round(record.money_earned, 2),
            'suggestion': record.get_health_suggestion()
        })
    
    return render_template('salary_thief_complete.html')

@poop_bp.route('/normal', methods=['GET', 'POST'])
@login_required
def normal_mode():
    """Normal Mode (no money tracking)"""
    if request.method == 'POST':
        data = request.get_json()
        datetime_str = data.get('datetime')
        duration = int(data.get('duration'))
        smell = data.get('smell')
        
        try:
            poop_datetime = datetime.fromisoformat(datetime_str)
        except:
            poop_datetime = datetime.utcnow()
        
        # Create record
        record = PoopRecord(
            user_id=current_user.id,
            datetime=poop_datetime,
            duration_minutes=duration,
            mode='normal',
            smell_condition=smell
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'record_id': record.id,
            'suggestion': record.get_health_suggestion()
        })
    
    return render_template('normal_mode_complete.html')

@poop_bp.route('/result/<int:record_id>')
@login_required
def result(record_id):
    """Show poop record result"""
    record = PoopRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return redirect(url_for('dashboard.index'))
    
    return render_template('poop_result.html', record=record)

# ======================== ANALYSIS ROUTES ========================
@analysis_bp.route('/dashboard')
@login_required
def analysis_dashboard():
    """Analysis dashboard"""
    # Get all records for user
    records = PoopRecord.query.filter_by(user_id=current_user.id).all()
    
    if not records:
        return render_template('analysis.html', 
                             avg_duration=0,
                             total_time=0,
                             health_score=0,
                             smell_distribution={},
                             records=[])
    
    # Calculate statistics
    avg_duration = sum(r.duration_minutes for r in records) / len(records)
    total_time = sum(r.duration_minutes for r in records)
    
    # Smell distribution
    smell_dist = {}
    for record in records:
        if record.smell_condition:
            smell_dist[record.smell_condition] = smell_dist.get(record.smell_condition, 0) + 1
    
    # Simple health score (0-100)
    # Based on: duration (ideal: 5-20 min), freshness, consistency
    health_score = calculate_health_score(records)
    
    return render_template('analysis.html',
                         avg_duration=round(avg_duration, 1),
                         total_time=total_time,
                         health_score=health_score,
                         smell_distribution=smell_dist,
                         records=records)

@analysis_bp.route('/export')
@login_required
def export_data():
    """Export user data as JSON"""
    records = PoopRecord.query.filter_by(user_id=current_user.id).all()
    
    data = {
        'user': {
            'username': current_user.username,
            'exported_at': datetime.utcnow().isoformat()
        },
        'records': [
            {
                'id': r.id,
                'datetime': r.datetime.isoformat(),
                'duration_minutes': r.duration_minutes,
                'mode': r.mode,
                'smell_condition': r.smell_condition,
                'money_earned': r.money_earned
            }
            for r in records
        ]
    }
    
    return jsonify(data)

# ======================== SETTINGS ROUTES ========================
@settings_bp.route('/')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html', user=current_user)

@settings_bp.route('/update', methods=['POST'])
@login_required
def update_settings():
    """Update user settings"""
    data = request.get_json()
    
    try:
        current_user.salary_amount = float(data.get('salary_amount', current_user.salary_amount))
        current_user.salary_currency = data.get('salary_currency', current_user.salary_currency)
        current_user.salary_type = data.get('salary_type', current_user.salary_type)
        current_user.working_days_per_week = int(data.get('working_days_per_week', current_user.working_days_per_week))
        current_user.working_hours_per_day = int(data.get('working_hours_per_day', current_user.working_hours_per_day))
        current_user.language = data.get('language', current_user.language)
        current_user.country = data.get('country', current_user.country)
        current_user.dark_mode = data.get('dark_mode', current_user.dark_mode)
        current_user.poop_reminder_enabled = data.get('poop_reminder_enabled', current_user.poop_reminder_enabled)
        current_user.privacy_mode_enabled = data.get('privacy_mode_enabled', current_user.privacy_mode_enabled)
        
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Settings updated!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ======================== HELPER FUNCTIONS ========================
def calculate_health_score(records):
    """Calculate simple health score (0-100)"""
    if not records:
        return 0
    
    score = 50  # Base score
    
    # Check duration (ideal: 5-20 minutes)
    durations = [r.duration_minutes for r in records]
    avg_duration = sum(durations) / len(durations)
    
    if 5 <= avg_duration <= 20:
        score += 25
    elif 3 <= avg_duration <= 30:
        score += 15
    
    # Check freshness/cleanliness
    fresh_count = sum(1 for r in records if r.smell_condition == 'fresh_clean')
    if len(records) > 0:
        freshness_ratio = fresh_count / len(records)
        score += int(freshness_ratio * 25)
    
    return min(100, max(0, score))

def check_achievements(user_id):
    """Check and award achievements"""
    user = User.query.get(user_id)
    
    # Check total salary thief time
    salary_records = PoopRecord.query.filter_by(user_id=user_id, mode='salary_thief').all()
    total_thief_minutes = sum(r.duration_minutes for r in salary_records)
    
    # Award achievements
    achievements_to_check = [
        ('salary_thief_10h', total_thief_minutes >= 600),
        ('salary_thief_50h', total_thief_minutes >= 3000),
        ('healthy_streak_7', check_health_streak(user_id, 7)),
        ('healthy_streak_30', check_health_streak(user_id, 30)),
        ('consistent_user_100', PoopRecord.query.filter_by(user_id=user_id).count() >= 100),
    ]
    
    for achievement_type, earned in achievements_to_check:
        if earned and not Achievement.query.filter_by(user_id=user_id, achievement_type=achievement_type).first():
            achievement = Achievement(user_id=user_id, achievement_type=achievement_type)
            db.session.add(achievement)
    
    db.session.commit()

def check_health_streak(user_id, days):
    """Check if user has a health streak of N days"""
    now = datetime.utcnow()
    streak_start = now - timedelta(days=days)
    
    records = PoopRecord.query.filter(
        PoopRecord.user_id == user_id,
        PoopRecord.datetime >= streak_start,
        PoopRecord.smell_condition == 'fresh_clean'
    ).all()
    
    return len(records) >= days
