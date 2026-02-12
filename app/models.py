from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import json

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # User settings
    salary_amount = db.Column(db.Float, default=10000.0)  # Default: NT$10,000/month
    salary_currency = db.Column(db.String(3), default='TWD')
    salary_type = db.Column(db.String(10), default='monthly')  # monthly or hourly
    working_days_per_week = db.Column(db.Integer, default=5)
    working_hours_per_day = db.Column(db.Integer, default=8)
    language = db.Column(db.String(5), default='en')
    country = db.Column(db.String(64), default='Taiwan')
    dark_mode = db.Column(db.Boolean, default=False)
    poop_reminder_enabled = db.Column(db.Boolean, default=False)
    privacy_mode_enabled = db.Column(db.Boolean, default=False)
    
    # Relationships
    poop_records = db.relationship('PoopRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def get_salary_per_minute(self):
        """Calculate salary per minute"""
        if self.salary_type == 'monthly':
            # Monthly ÷ (Working Days × 4.33 × Working Hours × 60)
            return self.salary_amount / (self.working_days_per_week * 4.33 * self.working_hours_per_day * 60)
        else:  # hourly
            # Hourly ÷ 60
            return self.salary_amount / 60

class PoopRecord(db.Model):
    """Poop record model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    duration_minutes = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(20), default='normal')  # 'salary_thief' or 'normal'
    smell_condition = db.Column(db.String(50), nullable=True)  # smell description
    money_earned = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def calculate_money(self, user=None):
        """Calculate money earned based on salary"""
        if user is None:
            user = self.user
        salary_per_minute = user.get_salary_per_minute()
        self.money_earned = self.duration_minutes * salary_per_minute
        return self.money_earned
    
    def get_health_suggestion(self):
        """Get health suggestion based on smell condition"""
        suggestions = {
            'fresh_clean': "Great digestion! Keep your current diet and hydration.",
            'extremely_smelly': "Try reducing red meat and increasing vegetables.",
            'rotten_meaty': "Consider reducing meat intake.",
            'sour': "Possible digestion imbalance. Avoid sugary drinks.",
            'chemical': "May indicate irritation. Drink more water.",
            'oily': "Reduce fried and oily food intake.",
            'egg_like': "Possible sulfur-rich food sensitivity. Monitor intake.",
            'sweet': "Watch sugar intake and monitor frequency."
        }
        return suggestions.get(self.smell_condition, "Keep monitoring your digestive health.")

class Achievement(db.Model):
    """Achievement/Trophy model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    achievement_type = db.Column(db.String(50), nullable=False)  # e.g., 'salary_thief_10h', 'healthy_streak_7'
    achieved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def get_title(self):
        """Get achievement title"""
        titles = {
            'salary_thief_10h': 'Master Salary Thief – 10 Hours',
            'salary_thief_50h': 'Professional Salary Thief – 50 Hours',
            'healthy_streak_7': 'Healthy Pooper – 7 Days Streak',
            'healthy_streak_30': 'Healthy Pooper – 30 Days Streak',
            'consistent_user_100': 'Century Club – 100 Records',
        }
        return titles.get(self.achievement_type, self.achievement_type)
    
    def get_description(self):
        """Get achievement description"""
        descriptions = {
            'salary_thief_10h': 'Accumulated 10 hours of salary thieving!',
            'salary_thief_50h': 'Became a professional salary thief with 50 hours!',
            'healthy_streak_7': 'Maintained healthy poops for 7 days!',
            'healthy_streak_30': 'Maintained healthy poops for 30 days!',
            'consistent_user_100': 'Recorded 100 poop sessions!',
        }
        return descriptions.get(self.achievement_type, '')
