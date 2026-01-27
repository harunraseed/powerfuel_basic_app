from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from functools import wraps
from config import Config
from supabase import create_client
import os
from datetime import datetime
from pdf_generator import generate_body_composition_pdf
from email_service import send_assessment_email
import math

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY', 'powerfuel-secret-key-2026-change-in-production')

# Initialize Supabase client
supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

# Admin credentials (in production, use database or environment variables)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Powerfuel@123'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def calculate_ideal_weight(height_cm, gender):
    """Calculate ideal weight using Devine formula"""
    height_inches = height_cm / 2.54
    if gender.lower() == 'male':
        # Men: IBW = 50 kg + 2.3 kg per inch over 5 feet
        ideal_weight = 50 + 2.3 * (height_inches - 60)
    else:
        # Women: IBW = 45.5 kg + 2.3 kg per inch over 5 feet
        ideal_weight = 45.5 + 2.3 * (height_inches - 60)
    return round(ideal_weight, 1)

def calculate_body_fat_category(body_fat_percent, gender):
    """Categorize body fat percentage"""
    if gender.lower() == 'male':
        if body_fat_percent < 6:
            return "Essential Fat"
        elif body_fat_percent < 14:
            return "Athletes"
        elif body_fat_percent < 18:
            return "Fitness"
        elif body_fat_percent < 25:
            return "Average"
        else:
            return "Obese"
    else:  # Female
        if body_fat_percent < 14:
            return "Essential Fat"
        elif body_fat_percent < 21:
            return "Athletes"
        elif body_fat_percent < 25:
            return "Fitness"
        elif body_fat_percent < 32:
            return "Average"
        else:
            return "Obese"

def calculate_lean_body_mass(weight_kg, body_fat_percent, gender, height_cm=None):
    """Calculate lean body mass using Boer formula for more accuracy"""
    if height_cm:
        # Boer formula (more accurate)
        if gender.lower() == 'male':
            # Men: LBM = 0.407 * weight + 0.267 * height - 19.2
            lbm = 0.407 * weight_kg + 0.267 * height_cm - 19.2
        else:
            # Women: LBM = 0.252 * weight + 0.473 * height - 48.3
            lbm = 0.252 * weight_kg + 0.473 * height_cm - 48.3
    else:
        # Simple calculation if height not provided
        lbm = weight_kg * (1 - body_fat_percent / 100)
    return round(lbm, 1)

def calculate_fat_mass(weight_kg, body_fat_percent):
    """Calculate fat mass"""
    return round(weight_kg * (body_fat_percent / 100), 1)

def get_bmi_reference(gender):
    """Get BMI reference values"""
    return {
        'athlete': {'min': 18.5, 'max': 24.9},
        'normal': {'min': 18.5, 'max': 24.9},
        'ranges': {
            'underweight': '< 18.5',
            'normal': '18.5 - 24.9',
            'overweight': '25.0 - 29.9',
            'obese': '≥ 30.0'
        }
    }

def get_body_fat_reference(gender):
    """Get body fat percentage reference values"""
    if gender.lower() == 'male':
        return {
            'athlete': {'min': 6, 'max': 13},
            'normal': {'min': 14, 'max': 24},
            'ranges': {
                'essential': '2-5%',
                'athletes': '6-13%',
                'fitness': '14-17%',
                'acceptable': '18-24%',
                'obese': '≥ 25%'
            }
        }
    else:  # Female
        return {
            'athlete': {'min': 14, 'max': 20},
            'normal': {'min': 21, 'max': 31},
            'ranges': {
                'essential': '10-13%',
                'athletes': '14-20%',
                'fitness': '21-24%',
                'acceptable': '25-31%',
                'obese': '≥ 32%'
            }
        }

def get_visceral_fat_reference():
    """Get visceral fat reference values (same for both genders)"""
    return {
        'athlete': {'min': 1, 'max': 9},
        'normal': {'min': 1, 'max': 12},
        'ranges': {
            'healthy': '1-12',
            'elevated': '13-15',
            'high': '≥ 16'
        }
    }

def get_bmi_category_asian_pacific(bmi, age):
    """Get BMI category based on Asian-Pacific classification (above 18 years)"""
    if age < 18:
        return "BMI classification not applicable for under 18 years"
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 23.0:
        return "Normal"
    elif bmi < 25.0:
        return "Overweight"
    elif bmi < 30.0:
        return "Obese I"
    else:
        return "Obese II"

def get_body_fat_status(body_fat_percent, gender):
    """Get body fat status based on research classification"""
    if gender.lower() == 'male':
        if body_fat_percent < 10:
            return "Low - Below normal range"
        elif body_fat_percent <= 20:
            return "Normal - Healthy range"
        elif body_fat_percent <= 25:
            return "High - Above normal"
        else:
            return "Very High - Action needed"
    else:  # Female
        if body_fat_percent < 20:
            return "Low - Below normal range"
        elif body_fat_percent <= 30:
            return "Normal - Healthy range"
        elif body_fat_percent <= 35:
            return "High - Above normal"
        else:
            return "Very High - Action needed"

def analyze_muscle_fat_ratio(subcutaneous, muscle):
    """Analyze subcutaneous fat to muscle mass ratio"""
    if muscle == 0:
        return "N/A", "Insufficient muscle mass"
    
    ratio = subcutaneous / muscle
    
    # Format ratio (e.g., 1:1.5 means 1 part fat to 1.5 parts muscle)
    ratio_text = f"1:{muscle/subcutaneous:.1f}" if subcutaneous > 0 else "0:1"
    
    # Ideal ratio for athletes is approximately 1:2 to 1:3 (more muscle than fat)
    if ratio <= 0.33:  # 1:3 or better
        status = "Excellent - Optimal ratio for athletes"
    elif ratio <= 0.5:  # 1:2
        status = "Good - Healthy ratio for active individuals"
    elif ratio <= 0.7:  # ~1:1.4
        status = "Fair - Room for improvement"
    elif ratio <= 1.0:  # 1:1
        status = "Average - Consider increasing muscle mass"
    else:
        status = "Below optimal - Focus on reducing fat and building muscle"
    
    return ratio_text, status

def get_visceral_fat_inference(visceral_fat):
    """Get visceral fat inference based on healthcare standards"""
    if visceral_fat <= 9.5:
        return "Normal - Healthy level"
    elif visceral_fat <= 14.5:
        return "High - Monitor and take action"
    else:
        return "Very High - Immediate action required"

def generate_runner_inference(assessment):
    """Generate comprehensive inference for runners/marathon athletes"""
    bmi = assessment['bmi']
    age = assessment['age']
    gender = assessment['gender']
    body_fat = assessment['body_fat_percent']
    visceral_fat = assessment['visceral_fat_percent']
    metabolic_age = assessment['metabolic_age']
    
    # BMI Category
    bmi_category = get_bmi_category_asian_pacific(bmi, age)
    
    # Consolidated Body Fat Status
    body_fat_status = get_body_fat_status(body_fat, gender)
    
    # Visceral Fat Inference
    visceral_inference = get_visceral_fat_inference(visceral_fat)
    
    # Muscle Mass Distribution Analysis
    muscle_distribution = {
        'whole_body': {
            'subcutaneous': assessment['whole_body_subcutaneous'],
            'muscle': assessment['whole_body_muscle'],
            'ratio': analyze_muscle_fat_ratio(assessment['whole_body_subcutaneous'], assessment['whole_body_muscle'])[0],
            'suggestion': analyze_muscle_fat_ratio(assessment['whole_body_subcutaneous'], assessment['whole_body_muscle'])[1]
        },
        'trunk': {
            'subcutaneous': assessment['trunk_subcutaneous'],
            'muscle': assessment['trunk_muscle'],
            'ratio': analyze_muscle_fat_ratio(assessment['trunk_subcutaneous'], assessment['trunk_muscle'])[0],
            'suggestion': analyze_muscle_fat_ratio(assessment['trunk_subcutaneous'], assessment['trunk_muscle'])[1]
        },
        'arms': {
            'subcutaneous': assessment['arms_subcutaneous'],
            'muscle': assessment['arms_muscle'],
            'ratio': analyze_muscle_fat_ratio(assessment['arms_subcutaneous'], assessment['arms_muscle'])[0],
            'suggestion': analyze_muscle_fat_ratio(assessment['arms_subcutaneous'], assessment['arms_muscle'])[1]
        },
        'legs': {
            'subcutaneous': assessment['legs_subcutaneous'],
            'muscle': assessment['legs_muscle'],
            'ratio': analyze_muscle_fat_ratio(assessment['legs_subcutaneous'], assessment['legs_muscle'])[0],
            'suggestion': analyze_muscle_fat_ratio(assessment['legs_subcutaneous'], assessment['legs_muscle'])[1]
        }
    }
    
    # Performance inference for runners
    performance_notes = []
    
    if bmi < 18.5:
        performance_notes.append("⚠️ Low BMI may indicate insufficient energy for endurance training. Consider nutritional consultation.")
    elif 18.5 <= bmi < 23:
        performance_notes.append("✓ BMI in optimal range for endurance athletes.")
    elif bmi >= 25:
        performance_notes.append("⚠️ Higher BMI may impact running efficiency and joint stress. Weight management recommended.")
    
    if visceral_fat <= 9.5:
        performance_notes.append("✓ Excellent visceral fat level - optimal for cardiovascular endurance.")
    else:
        performance_notes.append("⚠️ Elevated visceral fat may impact cardiovascular performance and recovery.")
    
    if metabolic_age < age:
        performance_notes.append(f"✓ Metabolic age ({metabolic_age}) is better than chronological age - excellent fitness level.")
    elif metabolic_age > age:
        performance_notes.append(f"⚠️ Metabolic age ({metabolic_age}) is higher than chronological age - focus on improving metabolic health.")
    
    # Body fat specific for runners
    if gender.lower() == 'male':
        if body_fat <= 13:
            performance_notes.append("✓ Body fat percentage optimal for competitive marathon running.")
        elif body_fat <= 17:
            performance_notes.append("Good body composition for recreational running.")
        else:
            performance_notes.append("⚠️ Body fat reduction may improve running performance and reduce injury risk.")
    else:
        if body_fat <= 20:
            performance_notes.append("✓ Body fat percentage optimal for competitive marathon running.")
        elif body_fat <= 24:
            performance_notes.append("Good body composition for recreational running.")
        else:
            performance_notes.append("⚠️ Body fat reduction may improve running performance and reduce injury risk.")
    
    return {
        'bmi_category': bmi_category,
        'body_fat_status': body_fat_status,
        'visceral_inference': visceral_inference,
        'muscle_distribution': muscle_distribution,
        'performance_notes': performance_notes
    }

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/form')
@login_required
def form():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/assessments', methods=['GET'])
@login_required
def get_assessments():
    try:
        search = request.args.get('search', '')
        
        if search:
            # Search by name, email, or mobile
            result = supabase.table('body_assessments').select('*').or_(
                f"name.ilike.%{search}%,email.ilike.%{search}%,mobile.ilike.%{search}%"
            ).order('created_at', desc=True).execute()
        else:
            # Get all assessments
            result = supabase.table('body_assessments').select('*').order('created_at', desc=True).execute()
        
        return jsonify({
            'success': True,
            'data': result.data
        })
    except Exception as e:
        print(f"Error fetching assessments: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/save-assessment', methods=['POST'])
@login_required
def save_assessment():
    try:
        data = request.json
        
        # Prepare data for database
        assessment_data = {
            'name': data['name'],
            'age': int(data['age']),
            'height_cm': float(data['height']),
            'gender': data['gender'],
            'mobile': data['mobile'],
            'email': data['email'],
            'weight_kg': float(data['weight']),
            'bmi': float(data['bmi']),
            'body_fat_percent': float(data['bodyFat']),
            'visceral_fat_percent': float(data['visceralFat']),
            'resting_metabolism': int(data['restingMetabolism']),
            'metabolic_age': int(data['metabolicAge']),
            'whole_body_subcutaneous': float(data['wholeBodySubcutaneous']),
            'whole_body_muscle': float(data['wholeBodyMuscle']),
            'trunk_subcutaneous': float(data['trunkSubcutaneous']),
            'trunk_muscle': float(data['trunkMuscle']),
            'arms_subcutaneous': float(data['armsSubcutaneous']),
            'arms_muscle': float(data['armsMuscle']),
            'legs_subcutaneous': float(data['legsSubcutaneous']),
            'legs_muscle': float(data['legsMuscle']),
            'created_at': datetime.now().isoformat()
        }
        
        # Insert into Supabase
        result = supabase.table('body_assessments').insert(assessment_data).execute()
        
        if result.data:
            assessment_id = result.data[0]['id']
            return jsonify({
                'success': True,
                'message': 'Assessment saved successfully',
                'assessment_id': assessment_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save assessment'
            }), 500
            
    except Exception as e:
        print(f"Error saving assessment: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/generate-pdf/<int:assessment_id>')
@login_required
def generate_pdf(assessment_id):
    try:
        # Fetch assessment data from Supabase
        result = supabase.table('body_assessments').select('*').eq('id', assessment_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'message': 'Assessment not found'}), 404
        
        assessment = result.data[0]
        
        # Generate PDF
        pdf_path = generate_body_composition_pdf(assessment)
        
        return send_file(pdf_path, as_attachment=True, download_name=f"body_assessment_{assessment['name'].replace(' ', '_')}.pdf")
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/send-email/<int:assessment_id>', methods=['POST'])
@login_required
def send_email(assessment_id):
    try:
        # Fetch assessment data from Supabase
        result = supabase.table('body_assessments').select('*').eq('id', assessment_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'message': 'Assessment not found'}), 404
        
        assessment = result.data[0]
        
        # Generate PDF
        pdf_path = generate_body_composition_pdf(assessment)
        
        # Send email
        send_assessment_email(
            to_email=assessment['email'],
            client_name=assessment['name'],
            pdf_path=pdf_path
        )
        
        # Update email_sent status in database
        supabase.table('body_assessments').update({
            'email_sent': True,
            'email_sent_at': datetime.now().isoformat()
        }).eq('id', assessment_id).execute()
        
        return jsonify({
            'success': True,
            'message': f'Assessment report sent to {assessment["email"]}'
        })
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/calculate-additional', methods=['POST'])
@login_required
def calculate_additional():
    """Calculate additional body composition metrics"""
    try:
        data = request.json
        weight = float(data['weight'])
        height = float(data['height'])
        gender = data['gender']
        body_fat = float(data['bodyFat'])
        
        calculations = {
            'bmi': calculate_bmi(weight, height),
            'idealWeight': calculate_ideal_weight(height, gender),
            'leanBodyMass': calculate_lean_body_mass(weight, body_fat, gender, height),
            'fatMass': calculate_fat_mass(weight, body_fat),
            'bodyFatCategory': calculate_body_fat_category(body_fat, gender)
        }
        
        return jsonify(calculations)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/reference-values/<gender>', methods=['GET'])
@login_required
def get_reference_values(gender):
    """Get reference values for body composition metrics"""
    try:
        return jsonify({
            'bmi': get_bmi_reference(gender),
            'bodyFat': get_body_fat_reference(gender),
            'visceralFat': get_visceral_fat_reference()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/inference/<int:assessment_id>', methods=['GET'])
@login_required
def get_inference(assessment_id):
    """Get inference for a specific assessment"""
    try:
        # Fetch assessment data from Supabase
        result = supabase.table('body_assessments').select('*').eq('id', assessment_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'message': 'Assessment not found'}), 404
        
        assessment = result.data[0]
        inference = generate_runner_inference(assessment)
        
        return jsonify({
            'success': True,
            'assessment': assessment,
            'inference': inference
        })
    except Exception as e:
        print(f"Error getting inference: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/delete-assessment/<int:assessment_id>', methods=['DELETE'])
@login_required
def delete_assessment(assessment_id):
    """Delete an assessment"""
    try:
        result = supabase.table('body_assessments').delete().eq('id', assessment_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Assessment deleted successfully'
        })
    except Exception as e:
        print(f"Error deleting assessment: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
