#!/bin/bash
# Make Money by Shit - Setup & Run Script for Linux/Mac

echo "🚀 Make Money by Shit - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python installation..."
python3 --version || { echo "❌ Python 3 is required but not installed."; exit 1; }

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "✓ Initializing database..."
python init_db.py

# Done
echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application, run:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "📱 Open http://localhost:5000 in your browser"
echo ""
echo "🔐 Default credentials:"
echo "   Username: shit"
echo "   Password: money"
