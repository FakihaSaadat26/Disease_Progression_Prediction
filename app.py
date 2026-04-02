"""
Simple Flask Web App for Disease Progression Prediction
Based on patient admission data
"""

import os
import json
from flask import Flask, render_template, jsonify, request
from data_processor import DataAnalyzer
from config import ADMISSIONS_FILE, LABITEMS_FILE, FLASK_HOST, FLASK_PORT, MAX_ROWS_DISPLAY

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize data analyzer
data_analyzer = None

try:
    data_folder = os.path.dirname(os.path.abspath(__file__))
    data_analyzer = DataAnalyzer(data_folder)
    data_analyzer.load_data()
    print("✓ Data loaded successfully")
except Exception as e:
    print(f"✗ Error initializing data: {e}")


# ============================================================================
# Simple Disease Progression Logic
# ============================================================================

def predict_disease_progression(patient_data):
    """
    Simple prediction based on admission data
    Returns: stage (0-4), confidence, recommendations
    """
    if not patient_data:
        return {'stage': 0, 'confidence': 0.0, 'recommendations': ['Patient not found']}
    
    stage = 0
    confidence = 0.5
    
    # Analyze admission type for severity
    admission_type = str(patient_data.get('admission_type', '')).lower()
    
    if 'emergency' in admission_type:
        stage = 2
        confidence = 0.7
    elif 'urgent' in admission_type:
        stage = 1
        confidence = 0.6
    elif 'elective' in admission_type:
        stage = 0
        confidence = 0.8
    
    # Check for readmission flag
    readmit = str(patient_data.get('has_chartevents_data', '')).lower()
    if readmit == 'y':
        stage = min(stage + 1, 4)
        confidence = min(confidence + 0.2, 1.0)
    
    return {
        'stage': stage,
        'confidence': confidence,
        'admission_type': admission_type
    }


def get_recommendations(stage):
    """Get recommendations based on disease stage"""
    recommendations = {
        0: [
            "✓ Patient appears stable",
            "Continue regular monitoring",
            "Maintain current treatment plan",
            "Routine follow-up in 3 months"
        ],
        1: [
            "⚠ Mild disease progression detected",
            "Increase monitoring frequency to monthly",
            "Review medication compliance",
            "Consider specialist referral"
        ],
        2: [
            "⚠⚠ Moderate disease progression",
            "Weekly monitoring recommended",
            "Medication adjustment may be needed",
            "Specialist consultation strongly advised"
        ],
        3: [
            "🚨 Severe disease progression",
            "Immediate specialist consultation required",
            "Daily or every-other-day monitoring",
            "Consider hospitalization assessment"
        ],
        4: [
            "🚨🚨 Critical condition",
            "URGENT: Immediate medical intervention needed",
            "ICU-level care may be required",
            "Emergency specialist consultation"
        ]
    }
    return recommendations.get(stage, [])


# ============================================================================
# ROUTES - Page Rendering
# ============================================================================

@app.route('/')
def index():
    """Home page with prediction form"""
    return render_template('index.html')


@app.route('/explore')
def explore():
    """Data exploration page"""
    return render_template('explore.html')


# ============================================================================
# ROUTES - API Endpoints
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict disease progression for a patient"""
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'patient_id required'}), 400
        
        if data_analyzer is None or data_analyzer.admissions is None:
            return jsonify({'error': 'Data not loaded'}), 500
        
        # Find patient in admissions data
        patient_records = data_analyzer.admissions[
            data_analyzer.admissions['subject_id'] == int(patient_id)
        ]
        
        if len(patient_records) == 0:
            return jsonify({'error': f'Patient {patient_id} not found'}), 404
        
        # Get latest admission record
        latest_record = patient_records.iloc[-1].to_dict()
        
        # Make prediction
        prediction = predict_disease_progression(latest_record)
        stage = prediction['stage']
        
        return jsonify({
            'patient_id': patient_id,
            'stage': stage,
            'stage_name': f'Stage {stage}',
            'confidence': prediction['confidence'],
            'admission_type': prediction['admission_type'],
            'recommendations': get_recommendations(stage),
            'patient_data': {
                'admission_type': latest_record.get('admission_type'),
                'insurance': latest_record.get('insurance'),
                'religion': latest_record.get('religion'),
                'marital_status': latest_record.get('marital_status'),
                'diagnosis': latest_record.get('diagnosis', 'N/A'),
            }
        })
    
    except ValueError:
        return jsonify({'error': 'Invalid patient ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/patient/<int:patient_id>')
def get_patient(patient_id):
    """Get patient details"""
    try:
        if data_analyzer is None or data_analyzer.admissions is None:
            return jsonify({'error': 'Data not loaded'}), 500
        
        patient_records = data_analyzer.admissions[
            data_analyzer.admissions['subject_id'] == patient_id
        ]
        
        if len(patient_records) == 0:
            return jsonify({'error': 'Patient not found'}), 404
        
        records = patient_records.to_dict('records')
        return jsonify({
            'patient_id': patient_id,
            'admission_count': len(records),
            'records': records
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admissions/summary')
def admissions_summary():
    """Get summary statistics of admissions data"""
    if data_analyzer is None or data_analyzer.admissions is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    summary = data_analyzer.get_admissions_summary()
    return jsonify(summary)


@app.route('/api/labitems/summary')
def labitems_summary():
    """Get summary statistics of lab items data"""
    if data_analyzer is None or data_analyzer.labitems is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    summary = data_analyzer.get_labitems_summary()
    return jsonify(summary)


@app.route('/api/admissions/data')
def admissions_data():
    """Get admissions data (paginated)"""
    if data_analyzer is None or data_analyzer.admissions is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 100, type=int)
    limit = min(limit, MAX_ROWS_DISPLAY)
    
    offset = (page - 1) * limit
    data = data_analyzer.admissions.iloc[offset:offset+limit].to_dict('records')
    
    return jsonify({
        'data': data,
        'page': page,
        'limit': limit,
        'total': len(data_analyzer.admissions)
    })


@app.route('/api/labitems/data')
def labitems_data():
    """Get lab items data (paginated)"""
    if data_analyzer is None or data_analyzer.labitems is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 100, type=int)
    limit = min(limit, MAX_ROWS_DISPLAY)
    
    offset = (page - 1) * limit
    data = data_analyzer.labitems.iloc[offset:offset+limit].to_dict('records')
    
    return jsonify({
        'data': data,
        'page': page,
        'limit': limit,
        'total': len(data_analyzer.labitems)
    })


@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'data_loaded': data_analyzer is not None
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print(f"Starting Flask app on {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
