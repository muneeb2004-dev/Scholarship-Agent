# 🎓 AI Scholarship Finder

An intelligent scholarship discovery platform powered by Flask and advanced AI, that finds and matches international scholarship opportunities tailored to your profile.

## ✨ Features

### Core Features
- **Smart Scholarship Search** - Browse 40+ scholarships from multiple international databases
- **AI-Powered Matching** - Intelligent ranking based on your profile (country, degree, field, GPA)
- **Real-Time Data** - Pulls fresh scholarship listings from live sources (RSS feeds, web scrapers)
- **Multiple Sources** - Combines data from DAAD, Fulbright, Chevening, Erasmus, and more
- **Parallel Processing** - Fast search using concurrent scraping
- **Excel Export** - Download scholarship results in spreadsheet format

### Advanced Features
- **REST API** - Full-featured JSON API for programmatic access
- **AI Recommendations** - Personalized scholarship recommendations based on extended profile
- **Advanced Filtering** - Filter by funding amount, deadline, keywords, and more
- **Search History** - Store and retrieve previous searches
- **Statistics & Analytics** - Track trends in scholarship opportunities
- **Rate Limiting** - API rate limiting for fair usage
- **Caching** - Performance optimization with intelligent caching
- **Database Persistence** - SQLite database for storing searches and history

### Web Interface
- **Modern UI** - Clean, responsive Bootstrap 5 interface
- **Real-time Search** - Live scholarship search with progress tracking
- **Interactive Dashboard** - View statistics and trends
- **Mobile Friendly** - Works seamlessly on desktop and mobile devices

## 🎯 What It Does

1. **Collects Data** - Scrapes and aggregates scholarships from 10+ international databases
2. **Processes Data** - Cleans, deduplicates, and standardizes scholarship records
3. **Matches Profiles** - Uses intelligent AI algorithms to rank scholarships by relevance to your profile
4. **Displays Results** - Shows ranked scholarships with match percentage and detailed information
5. **Provides APIs** - Exposes functionality through comprehensive REST APIs

## 🔧 How the Matching Works

Scholarships are scored (0-100%) based on:
- **Country Match** (30%) - Your preferred study destination
- **Degree Level** (25%) - Bachelor's, Master's, PhD, etc.
- **Field of Study** (20%) - Engineering, CS, Business, Medicine, etc.
- **CGPA/GPA** (15%) - Your academic performance
- **Funding Coverage** (10%) - Full, partial, or merit-based scholarships

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/scholarship_ai_agent.git
cd scholarship_ai_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from utils.db_manager import DatabaseManager; DatabaseManager().init_db()"

# Run Flask app
python flask_app.py
```

Visit: **http://localhost:5000**

## 🌐 Deployment

### PythonAnywhere (Recommended for Free Tier)

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed PythonAnywhere deployment instructions.

**Quick Summary:**
1. Push code to GitHub
2. Create PythonAnywhere account
3. Clone repo in PythonAnywhere bash console
4. Configure WSGI file
5. Reload web app

### Docker

```bash
docker build -t scholarship-finder .
docker run -p 5000:5000 scholarship-finder
```

### Manual Server

```bash
# Using Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

## 💻 Tech Stack

**Backend:**
- **Framework**: Flask 3.0 with REST API
- **Database**: SQLite (upgrade to PostgreSQL for production)
- **Caching**: Flask-Caching
- **Rate Limiting**: Flask-Limiter
- **Web Scraping**: BeautifulSoup4, requests, feedparser
- **Data Processing**: Pandas, openpyxl

**Frontend:**
- **UI Framework**: Bootstrap 5
- **HTTP Client**: Axios
- **Styling**: Custom CSS with gradient themes

**AI/ML:**
- **Recommendation Engine**: Custom rule-based AI
- **Matching Algorithm**: Multi-factor scoring system
- **Analytics**: Database-backed statistics

## 📚 API Usage

The application provides a comprehensive REST API. See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for full details.

### Example API Call

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "degree_level": "Master'"'"'s",
    "field_of_study": "Computer Science & IT",
    "nationality": "Pakistani",
    "cgpa": 3.8,
    "country": "Germany"
  }'
```

## 📋 Scholarship Sources

- **DAAD** (Germany) - International scholarship database
- **Fulbright** (USA) - US government scholarships
- **Chevening** (UK) - UK Foreign Office scholarships
- **Erasmus+** (Europe) - European mobility program
- **Commonwealth** (UK/Commonwealth) - Commonwealth scholarships
- **HEC Pakistan** - Pakistani university scholarships
- **Online Scholarship Databases** - Aggregated sources
- Scholars4Dev
- Opportunities Corners
- Youth Opportunities
- ScholarshipPortal

## � Credits

**Developed by:**
- Muhammad Abdullah
- Muneeb Tahir 

This project is a collaborative effort combining web scraping, intelligent matching algorithms, and user-friendly interface design.

## �📄 License

MIT License
