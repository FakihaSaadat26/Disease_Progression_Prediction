#!/bin/bash
# Disease Progression Prediction - Web Frontend Starter
# This script installs dependencies and runs the Flask web app

echo "========================================"
echo "Disease Progression Prediction System"
echo "Web Frontend Starter"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

echo "[1/3] Installing/Updating dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/3] Starting Flask web server..."
echo ""
echo "============================================"
echo "Web app is starting at:"
echo "http://localhost:5000"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

sleep 2

# Start Flask app
python3 app.py
