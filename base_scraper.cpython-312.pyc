# config/flask_config.py - Flask Configuration

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    JSON_SORT_KEYS = False
    
    # Caching
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/scholarships.db')
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Features
    ENABLE_EXPORT = os.environ.get('ENABLE_EXPORT', 'True').lower() == 'true'
    ENABLE_HISTORY = os.environ.get('ENABLE_HISTORY', 'True').lower() == 'true'
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'True').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    CACHE_TYPE = 'simple'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    CACHE_TYPE = 'simple'  # Use Redis for production
    
    # Stricter security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'


# Get config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Get configuration class"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
