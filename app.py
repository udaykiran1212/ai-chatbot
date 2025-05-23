from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from functools import wraps
import jwt
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key-for-development')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')

# Configure Gemini
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Gemini API configured successfully")
    else:
        logger.warning("GEMINI_API_KEY not found in environment variables")
except Exception as e:
    logger.error(f"Error configuring Gemini: {str(e)}")

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
            return f(current_user, *args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'message': 'Token is invalid'}), 401
    return decorated

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': 'Failed to load page'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        # TODO: Implement user registration logic
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        # TODO: Implement login logic
        token = jwt.encode({'user': data.get('username')}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/generate', methods=['GET'])
@token_required
def generate_quiz(current_user):
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                'question': 'What is the capital of France?',
                'options': ['Paris', 'London', 'Berlin', 'Madrid'],
                'correct_answer': 0
            })
            
        # Generate quiz using Gemini
        prompt = "Generate a geography quiz question about world geography. Include the correct answer and 3 incorrect options."
        response = model.generate_content(prompt)
        
        # TODO: Parse response and format quiz question
        return jsonify({
            'question': 'Sample question',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correct_answer': 0
        })
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    try:
        data = request.get_json()
        if not data or 'answer' not in data:
            return jsonify({'error': 'Missing answer'}), 400
        # TODO: Implement quiz submission logic
        return jsonify({'message': 'Answer submitted successfully'})
    except Exception as e:
        logger.error(f"Quiz submission error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    try:
        # TODO: Implement progress tracking logic
        return jsonify({'score': 0, 'completed_quizzes': 0})
    except Exception as e:
        logger.error(f"Progress tracking error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# This is required for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True) 
