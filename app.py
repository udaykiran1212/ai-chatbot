from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from functools import wraps
import jwt
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    # TODO: Implement user registration logic
    return jsonify({'message': 'Registration endpoint'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # TODO: Implement login logic
    return jsonify({'message': 'Login endpoint'})

@app.route('/api/quiz/generate', methods=['GET'])
@token_required
def generate_quiz(current_user):
    try:
        # Generate quiz using Gemini
        prompt = "Generate a geography quiz question about world geography. Include the correct answer and 3 incorrect options."
        response = model.generate_content(prompt)
        
        # TODO: Parse response and format quiz question
        return jsonify({
            'question': 'Sample question',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correct_answer': 'Option 1'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    # TODO: Implement quiz submission logic
    return jsonify({'message': 'Quiz submission endpoint'})

@app.route('/api/quiz/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    # TODO: Implement progress tracking logic
    return jsonify({'message': 'Progress tracking endpoint'})

if __name__ == '__main__':
    app.run(debug=True) 