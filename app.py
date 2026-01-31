from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Sample projects data (hardcoded - no database needed)
SAMPLE_PROJECTS = [
    {
        'id': 1,
        'title': 'Python Automation Tool',
        'description': 'A Python script that automates daily tasks and saves time. Built with Python to handle file organization and data processing.',
        'technologies': ['Python', 'Automation'],
        'github_url': 'https://github.com/Mazin-Sayed/automation-tool',
        'demo_url': None,
        'image_url': None,
        'created_at': '2026-01-01'
    },
    {
        'id': 2,
        'title': 'Personal Website',
        'description': 'A clean and responsive website built from scratch using HTML and CSS. Features modern design and smooth animations.',
        'technologies': ['HTML', 'CSS', 'JavaScript'],
        'github_url': 'https://github.com/Mazin-Sayed/personal-website',
        'demo_url': None,
        'image_url': None,
        'created_at': '2026-01-01'
    }
]

# Store messages in memory (temporary - for demo purposes)
contact_messages = []

# API Routes

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify(SAMPLE_PROJECTS), 200

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    project = next((p for p in SAMPLE_PROJECTS if p['id'] == project_id), None)
    if project:
        return jsonify(project), 200
    else:
        return jsonify({'error': 'Project not found'}), 404

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit a contact form"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Store message (temporary)
        message_data = {
            'id': len(contact_messages) + 1,
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'created_at': datetime.now().isoformat()
        }
        contact_messages.append(message_data)
        
        # Log to console (you'll see this in Vercel logs)
        print(f"📧 New Contact Message:")
        print(f"From: {data['name']} <{data['email']}>")
        print(f"Subject: {data['subject']}")
        print(f"Message: {data['message']}")
        
        return jsonify({'message': 'Message sent successfully! Thank you for reaching out.'}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to send message. Please try again.'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact messages"""
    return jsonify(contact_messages), 200

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    skills = [
        {'id': 1, 'category': 'Good At', 'name': 'HTML & CSS', 'level': 90},
        {'id': 2, 'category': 'Good At', 'name': 'Python', 'level': 85},
        {'id': 3, 'category': 'Good At', 'name': 'JavaScript', 'level': 80},
        {'id': 4, 'category': 'Learning', 'name': 'Machine Learning', 'level': 70},
        {'id': 5, 'category': 'Learning', 'name': 'Automation', 'level': 75}
    ]
    return jsonify(skills), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Portfolio API is running',
        'version': '3.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Mazin Sayed Portfolio API',
        'version': '3.0.0',
        'endpoints': {
            'projects': '/api/projects',
            'contact': '/api/contact',
            'skills': '/api/skills',
            'health': '/api/health'
        }
    }), 200

# For local development
if __name__ == '__main__':
    print('🚀 Starting Flask server...')
    print('💻 API available at: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
