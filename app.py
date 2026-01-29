from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Database configuration
DATABASE = 'portfolio.db'

def get_db():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technologies TEXT NOT NULL,
            github_url TEXT,
            demo_url TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            level INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample projects if table is empty
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        sample_projects = [
            (
                'AI Image Recognition',
                'Deep learning model for image classification using CNN architecture. Achieved 95% accuracy on test dataset.',
                json.dumps(['Python', 'TensorFlow', 'OpenCV', 'Flask']),
                'https://github.com/aidev/image-recognition',
                'https://demo.aidev.com/image-recognition',
                None
            ),
            (
                'Real-time Chat Application',
                'Full-stack chat app with WebSocket support, user authentication, and message encryption.',
                json.dumps(['React', 'Node.js', 'Socket.io', 'MongoDB']),
                'https://github.com/aidev/chat-app',
                'https://chat.aidev.com',
                None
            ),
            (
                'Predictive Analytics Dashboard',
                'Interactive dashboard for data visualization and predictive modeling using machine learning algorithms.',
                json.dumps(['Python', 'Pandas', 'Plotly', 'Scikit-learn']),
                'https://github.com/aidev/analytics-dashboard',
                None,
                None
            ),
            (
                'E-commerce Platform',
                'Modern e-commerce solution with payment integration, inventory management, and admin dashboard.',
                json.dumps(['Vue.js', 'Django', 'PostgreSQL', 'Stripe']),
                'https://github.com/aidev/ecommerce',
                'https://shop.aidev.com',
                None
            ),
            (
                'NLP Sentiment Analysis',
                'Natural language processing tool for analyzing sentiment in social media posts and reviews.',
                json.dumps(['Python', 'NLTK', 'Transformers', 'FastAPI']),
                'https://github.com/aidev/sentiment-analysis',
                None,
                None
            ),
            (
                'Smart Home Automation',
                'IoT-based home automation system with voice control and mobile app integration.',
                json.dumps(['Python', 'React Native', 'MQTT', 'Raspberry Pi']),
                'https://github.com/aidev/smart-home',
                None,
                None
            )
        ]
        
        cursor.executemany('''
            INSERT INTO projects (title, description, technologies, github_url, demo_url, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_projects)
    
    # Insert sample skills if table is empty
    cursor.execute('SELECT COUNT(*) FROM skills')
    if cursor.fetchone()[0] == 0:
        sample_skills = [
            ('AI & Machine Learning', 'Python', 95),
            ('AI & Machine Learning', 'TensorFlow', 88),
            ('AI & Machine Learning', 'PyTorch', 85),
            ('AI & Machine Learning', 'Scikit-learn', 90),
            ('Frontend Development', 'HTML/CSS', 95),
            ('Frontend Development', 'JavaScript', 92),
            ('Frontend Development', 'React', 88),
            ('Frontend Development', 'Vue.js', 82),
            ('Backend Development', 'Python/Flask', 90),
            ('Backend Development', 'Django', 85),
            ('Backend Development', 'Node.js', 80),
            ('Backend Development', 'SQL/NoSQL', 87)
        ]
        
        cursor.executemany('''
            INSERT INTO skills (category, name, level)
            VALUES (?, ?, ?)
        ''', sample_skills)
    
    conn.commit()
    conn.close()

# API Routes

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
        projects = cursor.fetchall()
        conn.close()
        
        projects_list = []
        for project in projects:
            projects_list.append({
                'id': project['id'],
                'title': project['title'],
                'description': project['description'],
                'technologies': json.loads(project['technologies']),
                'github_url': project['github_url'],
                'demo_url': project['demo_url'],
                'image_url': project['image_url'],
                'created_at': project['created_at']
            })
        
        return jsonify(projects_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        conn.close()
        
        if project:
            return jsonify({
                'id': project['id'],
                'title': project['title'],
                'description': project['description'],
                'technologies': json.loads(project['technologies']),
                'github_url': project['github_url'],
                'demo_url': project['demo_url'],
                'image_url': project['image_url'],
                'created_at': project['created_at']
            }), 200
        else:
            return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'description', 'technologies']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (title, description, technologies, github_url, demo_url, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['description'],
            json.dumps(data['technologies']),
            data.get('github_url'),
            data.get('demo_url'),
            data.get('image_url')
        ))
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'Project created successfully',
            'id': project_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build update query dynamically
        update_fields = []
        values = []
        
        if 'title' in data:
            update_fields.append('title = ?')
            values.append(data['title'])
        if 'description' in data:
            update_fields.append('description = ?')
            values.append(data['description'])
        if 'technologies' in data:
            update_fields.append('technologies = ?')
            values.append(json.dumps(data['technologies']))
        if 'github_url' in data:
            update_fields.append('github_url = ?')
            values.append(data['github_url'])
        if 'demo_url' in data:
            update_fields.append('demo_url = ?')
            values.append(data['demo_url'])
        if 'image_url' in data:
            update_fields.append('image_url = ?')
            values.append(data['image_url'])
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        values.append(project_id)
        query = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Project updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Project not found'}), 404
        
        conn.close()
        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit a contact form"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['subject'],
            data['message']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Message sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact messages"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
        contacts = cursor.fetchall()
        conn.close()
        
        contacts_list = []
        for contact in contacts:
            contacts_list.append({
                'id': contact['id'],
                'name': contact['name'],
                'email': contact['email'],
                'subject': contact['subject'],
                'message': contact['message'],
                'created_at': contact['created_at']
            })
        
        return jsonify(contacts_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills ORDER BY category, level DESC')
        skills = cursor.fetchall()
        conn.close()
        
        skills_list = []
        for skill in skills:
            skills_list.append({
                'id': skill['id'],
                'category': skill['category'],
                'name': skill['name'],
                'level': skill['level']
            })
        
        return jsonify(skills_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['POST'])
def add_skill():
    """Add a new skill"""
    try:
        data = request.get_json()
        
        required_fields = ['category', 'name', 'level']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO skills (category, name, level)
            VALUES (?, ?, ?)
        ''', (
            data['category'],
            data['name'],
            data['level']
        ))
        conn.commit()
        skill_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'Skill added successfully',
            'id': skill_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Portfolio API is running',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Portfolio API',
        'version': '1.0.0',
        'endpoints': {
            'projects': '/api/projects',
            'contact': '/api/contact',
            'skills': '/api/skills',
            'health': '/api/health'
        }
    }), 200

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DATABASE):
        print('Initializing database...')
        init_db()
        print('Database initialized successfully!')
    
    print('Starting Flask server...')
    print('API available at: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
