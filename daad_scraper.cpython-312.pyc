#!/bin/bash
# run.sh - Development startup script

echo "🎓 Starting AI Scholarship Finder..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python -c "from utils.db_manager import DatabaseManager; db = DatabaseManager(); db.init_db(); print('Database ready!')"

# Run Flask app
echo ""
echo "🚀 Starting Flask app..."
echo "📍 Visit http://localhost:5000"
echo ""

export FLASK_ENV=development
export FLASK_DEBUG=True

python flask_app.py
