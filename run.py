#!/usr/bin/env python
"""
Make Money by Shit - Main Application Entry Point
"""
import os
from app import create_app, db
from app.models import User

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make objects available in Flask shell"""
    return {'db': db, 'User': User}

@app.before_request
def before_request():
    """Before request hook"""
    pass

@app.after_request
def after_request(response):
    """After request hook"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return {
        'status': 'error',
        'message': 'Page not found',
        'code': 404
    }, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return {
        'status': 'error',
        'message': 'Internal server error',
        'code': 500
    }, 500

def init_db():
    """Initialize database with default user"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default user if not exists
        default_user = User.query.filter_by(username='shit').first()
        if not default_user:
            default_user = User(username='shit')
            default_user.set_password('money')
            db.session.add(default_user)
            db.session.commit()
            print("✅ Default user created: username=shit, password=money")
        else:
            print("ℹ️  Default user already exists")

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run development server
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
