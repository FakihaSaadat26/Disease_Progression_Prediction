"""
Configuration for Medical Data Analysis
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = PROJECT_ROOT

# Data files
ADMISSIONS_FILE = os.path.join(DATA_FOLDER, 'ADMISSIONS.csv')
LABITEMS_FILE = os.path.join(DATA_FOLDER, 'D_LABITEMS.csv')

# Flask config
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
DEBUG_MODE = True

# Data limits (for display)
MAX_ROWS_DISPLAY = 1000
