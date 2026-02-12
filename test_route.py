from app import create_app
from flask_login import FlaskLoginClient

app = create_app()
app.test_client_class = FlaskLoginClient

with app.test_client() as client:
    # First login
    response = client.post('/auth/login', data={
        'username': 'shit',
        'password': 'money'
    }, follow_redirects=True)
    
    print(f"Login response status: {response.status_code}")
    
    # Now try to access analysis page
    response = client.get('/analysis/dashboard', follow_redirects=True)
    print(f"Analysis page status: {response.status_code}")
    print(f"Final URL: {response.request.path}")
    
    # Check if page contains expected content
    data = response.get_data(as_text=True)
    if 'Poop Analysis' in data:
        print("✓ Found 'Poop Analysis' in response")
    else:
        print("✗ 'Poop Analysis' not found in response")
        
    if 'Recent Records' in data:
        print("✓ Found 'Recent Records' in response")
    else:
        print("✗ 'Recent Records' not found in response")
