# Configuration for PythonAnywhere deployment

# .pythonanywhere_config
# This file contains settings specific to PythonAnywhere deployment

import os
import sys

# Add project directory to path
project_home = u'/home/username/scholarship-agent'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment path (if using one)
activate_this = os.path.expanduser('~/venv/bin/activate_this.py')
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Set up environment
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Import Flask app
from flask_app import app as application

# Disable debug mode for production
application.config['DEBUG'] = False
