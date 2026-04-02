#!/usr/bin/env python3
"""
Simple launcher for Medical Data Analysis Web App
"""

import os
import sys
import webbrowser
from time import sleep

def main():
    """Launch the Flask web app"""
    print("\n" + "="*60)
    print("Medical Data Analysis - Simple Web App")
    print("="*60)
    
    # Check if data files exist
    data_folder = os.path.dirname(os.path.abspath(__file__))
    admissions_file = os.path.join(data_folder, 'ADMISSIONS.csv')
    labitems_file = os.path.join(data_folder, 'D_LABITEMS.csv')
    
    if not os.path.exists(admissions_file):
        print(f"✗ ADMISSIONS.csv not found at {admissions_file}")
        sys.exit(1)
    
    if not os.path.exists(labitems_file):
        print(f"✗ D_LABITEMS.csv not found at {labitems_file}")
        sys.exit(1)
    
    print("✓ Data files found")
    print(f"  - ADMISSIONS.csv")
    print(f"  - D_LABITEMS.csv")
    print()
    
    # Check dependencies
    try:
        import flask
        import pandas
        print("✓ Required packages installed")
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nInstall dependencies with:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("Starting Flask app...")
    print("Visit: http://127.0.0.1:5000")
    print()
    print("Press Ctrl+C to stop")
    print("="*60)
    print()
    
    # Launch web browser after a short delay
    try:
        sleep(2)
        webbrowser.open('http://127.0.0.1:5000')
    except:
        pass
    
    # Start Flask app
    from app import app
    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()
