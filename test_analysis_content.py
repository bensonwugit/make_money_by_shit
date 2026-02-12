from app import create_app
from flask import Flask

app = create_app()

# Create a test client
client = app.test_client()

# Make request with authentication context
with app.test_request_context('/'):
    from flask_login import current_user
    from app.models import User
    
    # Get user
    app.app_context().push()
    user = User.query.get(1)
    print(f"User found: {user.username if user else 'None'}")
    
    # Make request
    response = client.get('/analysis/dashboard')
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Length: {len(response.get_data())}")
    
    # Check content
    content = response.get_data(as_text=True)
    if 'Poop Analysis' in content:
        print("✓ Found 'Poop Analysis' title")
    else:
        print("✗ 'Poop Analysis' NOT found")
        
    if 'Recent Records' in content:
        print("✓ Found 'Recent Records' section")
    else:
        print("✗ 'Recent Records' NOT found")
        
    if 'Digestive Health Score' in content:
        print("✓ Found 'Digestive Health Score'")
    else:
        print("✗ 'Digestive Health Score' NOT found")

    # Print first 2000 characters
    print("\n--- First 2000 chars of response ---")
    print(content[:2000])
