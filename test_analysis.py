from app import create_app, db
from app.models import User, PoopRecord

app = create_app()

with app.app_context():
    # Get user 1
    user = User.query.get(1)
    if user:
        records = PoopRecord.query.filter_by(user_id=user.id).all()
        print(f"User: {user.username}")
        print(f"Records count: {len(records)}")
        for r in records:
            print(f"  Record {r.id}: {r.datetime}, {r.duration_minutes} min, {r.smell_condition}")
        
        # Calculate health score
        if records:
            from app.routes import calculate_health_score
            health_score = calculate_health_score(records)
            print(f"Health score: {health_score}")
