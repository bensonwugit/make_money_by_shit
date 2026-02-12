"""
Initialize the application and database
"""
from app import create_app, db
from app.models import User

def init():
    """Initialize the database"""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create default user
        default_user = User.query.filter_by(username='shit').first()
        if not default_user:
            default_user = User(username='shit')
            default_user.set_password('money')
            db.session.add(default_user)
            db.session.commit()
            print("✅ Default user created")
            print("   Username: shit")
            print("   Password: money")
        else:
            print("ℹ️  Default user already exists")

if __name__ == '__main__':
    init()
