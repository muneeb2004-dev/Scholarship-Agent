# flask_app.py - Flask Application with REST APIs

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Import our modules
from config.settings import *
from config.flask_config import get_config
from ai_engine.orchestrator import AIOrchestrator
from utils.excel_exporter import ExcelExporter
from utils.validators import InputValidator
from utils.db_manager import DatabaseManager

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='assets')

# Load configuration
config = get_config(os.environ.get('FLASK_ENV', 'development'))
app.config.from_object(config)

CORS(app)

# Initialize caching (Redis recommended for production, using simple cache for now)
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}
cache = Cache(app, config=cache_config)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize services
orchestrator = AIOrchestrator()
validator = InputValidator()
excel_exporter = ExcelExporter()
db_manager = DatabaseManager()

# Initialize database tables (runs on import for WSGI compatibility)
db_manager.init_db()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         countries=COUNTRIES, 
                         degrees=DEGREE_LEVELS,
                         fields=FIELDS_OF_STUDY,
                         nationalities=NATIONALITIES)


@app.route('/dashboard')
def dashboard():
    """Dashboard with statistics"""
    stats = db_manager.get_statistics()
    return render_template('dashboard.html', stats=stats)


# ==================== API ENDPOINTS ====================

@app.route('/api/search', methods=['POST'])
@limiter.limit("10 per hour")
def api_search():
    """
    Search for scholarships based on user profile
    
    JSON Body:
    {
        "degree_level": "Master's",
        "field_of_study": "Computer Science & IT",
        "nationality": "Pakistani",
        "cgpa": 3.8,
        "country": "Germany"
    }
    """
    try:
        profile = request.get_json()
        
        # Validate profile
        is_valid, errors = validator.validate_profile(profile)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        logger.info(f"Search initiated for profile: {profile}")
        
        # Execute search
        scholarships = orchestrator.search_scholarships(profile)
        
        # Save to database
        search_id = db_manager.save_search(profile, scholarships)
        
        # Cache the results
        cache.set(f"search_{search_id}", scholarships, timeout=3600)
        
        logger.info(f"Found {len(scholarships)} scholarships (search_id: {search_id})")
        
        return jsonify({
            'success': True,
            'search_id': search_id,
            'count': len(scholarships),
            'scholarships': scholarships,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/search/<search_id>', methods=['GET'])
@cache.cached(timeout=3600)
def api_get_search(search_id):
    """Retrieve previous search results"""
    try:
        search_data = db_manager.get_search(search_id)
        
        if not search_data:
            return jsonify({
                'success': False,
                'message': 'Search not found'
            }), 404
        
        return jsonify({
            'success': True,
            'search_id': search_id,
            'profile': search_data['profile'],
            'scholarships': search_data['scholarships'],
            'count': len(search_data['scholarships']),
            'created_at': search_data['created_at']
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving search: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/filter', methods=['POST'])
def api_filter():
    """
    Filter scholarships by additional criteria
    
    JSON Body:
    {
        "scholarships": [...],
        "filters": {
            "min_funding": 5000,
            "max_deadline_days": 90,
            "keywords": ["AI", "ML"]
        }
    }
    """
    try:
        data = request.get_json()
        scholarships = data.get('scholarships', [])
        filters = data.get('filters', {})
        
        filtered = orchestrator.filter_scholarships(scholarships, filters)
        
        return jsonify({
            'success': True,
            'count': len(filtered),
            'scholarships': filtered
        }), 200
    
    except Exception as e:
        logger.error(f"Filter error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/export', methods=['POST'])
@limiter.limit("5 per hour")
def api_export():
    """
    Export scholarships to Excel
    
    JSON Body:
    {
        "scholarships": [...],
        "filename": "my_scholarships"
    }
    """
    try:
        data = request.get_json()
        scholarships = data.get('scholarships', [])
        filename = data.get('filename', 'scholarships')
        
        if not scholarships:
            return jsonify({
                'success': False,
                'message': 'No scholarships provided'
            }), 400
        
        # Generate Excel file (returns full path in temp dir)
        filepath = excel_exporter.export_scholarships(scholarships, filename)
        
        # Extract just the filename for download
        download_name = filename if filename.endswith('.xlsx') else f"{filename}.xlsx"
        
        logger.info(f"Exported {len(scholarships)} scholarships to {filepath}")
        
        return send_file(filepath, 
                        as_attachment=True,
                        download_name=download_name)
    
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """
    Get AI-powered scholarship recommendations based on profile
    
    JSON Body:
    {
        "degree_level": "Master's",
        "field_of_study": "Computer Science & IT",
        "nationality": "Pakistani",
        "cgpa": 3.8,
        "country": "Germany",
        "work_experience_years": 2,
        "research_interests": ["AI", "ML"]
    }
    """
    try:
        profile = request.get_json()
        
        # Get recommendations using AI
        recommendations = orchestrator.get_ai_recommendations(profile)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
    
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/countries', methods=['GET'])
@cache.cached(timeout=86400)
def api_countries():
    """Get list of available countries"""
    return jsonify({
        'success': True,
        'countries': COUNTRIES
    }), 200


@app.route('/api/fields', methods=['GET'])
@cache.cached(timeout=86400)
def api_fields():
    """Get list of available fields of study"""
    return jsonify({
        'success': True,
        'fields': FIELDS_OF_STUDY
    }), 200


@app.route('/api/degrees', methods=['GET'])
@cache.cached(timeout=86400)
def api_degrees():
    """Get list of available degree levels"""
    return jsonify({
        'success': True,
        'degrees': DEGREE_LEVELS
    }), 200


@app.route('/api/nationalities', methods=['GET'])
@cache.cached(timeout=86400)
def api_nationalities():
    """Get list of available nationalities"""
    return jsonify({
        'success': True,
        'nationalities': NATIONALITIES
    }), 200


@app.route('/api/history', methods=['GET'])
def api_history():
    """Get user's search history (requires authentication in production)"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db_manager.get_search_history(limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        }), 200
    
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
@cache.cached(timeout=3600)
def api_stats():
    """Get application statistics"""
    try:
        stats = db_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Resource not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'status': 500
    }), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limiting"""
    return jsonify({
        'success': False,
        'message': 'Rate limit exceeded. Please try again later.',
        'status': 429
    }), 429


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    }), 200


# ==================== INITIALIZATION ====================

if __name__ == '__main__':
    # Create database tables
    db_manager.init_db()
    
    # Run Flask app
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=debug_mode,
        use_reloader=False  # Important for PythonAnywhere
    )
