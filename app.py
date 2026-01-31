from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Import psycopg2 for PostgreSQL (Supabase)
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Warning: psycopg2 not installed. Using in-memory storage only.")

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', '')

def get_db():
    """Create a database connection to Supabase PostgreSQL"""
    if not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize the database with required tables"""
    conn = get_db()
    if not conn:
        print("No database connection. Skipping initialization.")
        return
    
    try:
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                technologies JSONB NOT NULL,
                github_url TEXT,
                demo_url TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
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
                id SERIAL PRIMARY KEY,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if projects table is empty
        cursor.execute('SELECT COUNT(*) FROM projects')
        count = cursor.fetchone()[0]
        
        # Insert sample projects if table is empty
        if count == 0:
            sample_projects = [
                (
                    'AI Image Recognition',
                    'Deep learning model for image classification using CNN architecture. Achieved 95% accuracy on test dataset.',
                    json.dumps(['Python', 'TensorFlow', 'OpenCV', 'Flask']),
                    'https://github.com/Mazin-Sayed/image-recognition',
                    None,
                    None
                ),
                (
                    'Python Automation Tool',
                    'A Python script that automates daily tasks and saves time. Built with Python to handle file organization and data processing.',
                    json.dumps(['Python', 'Automation']),
                    'https://github.com/Mazin-Sayed/automation-tool',
                    None,
                    None
                ),
                (
                    'Personal Website',
                    'A clean and responsive website built from scratch using HTML and CSS. Features modern design and smooth animations.',
                    json.dumps(['HTML', 'CSS', 'JavaScript']),
                    'https://github.com/Mazin-Sayed/personal-website',
                    None,
                    None
                )
            ]
            
            cursor.executemany('''
                INSERT INTO projects (title, description, technologies, github_url, demo_url, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', sample_projects)
        
        conn.commit()
        cursor.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

# API Routes

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    conn = get_db()
    if not conn:
        # Return sample projects if no database
        return jsonify([
            {
                'id': 1,
                'title': 'Python Automation Tool',
                'description': 'A Python script that automates daily tasks and saves time.',
                'technologies': ['Python', 'Automation'],
                'github_url': '#',
                'demo_url': None,
                'image_url': None,
                'created_at': '2026-01-01'
            },
            {
                'id': 2,
                'title': 'Personal Website',
                'description': 'A clean and responsive website built from scratch using HTML and CSS.',
                'technologies': ['HTML', 'CSS'],
                'github_url': '#',
                'demo_url': None,
                'image_url': None,
                'created_at': '2026-01-01'
            }
        ]), 200
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        
        projects_list = []
        for project in projects:
            projects_list.append({
                'id': project['id'],
                'title': project['title'],
                'description': project['description'],
                'technologies': project['technologies'],
                'github_url': project['github_url'],
                'demo_url': project['demo_url'],
                'image_url': project['image_url'],
                'created_at': str(project['created_at']) if project['created_at'] else None
            })
        
        return jsonify(projects_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
        project = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if project:
            return jsonify({
                'id': project['id'],
                'title': project['title'],
                'description': project['description'],
                'technologies': project['technologies'],
                'github_url': project['github_url'],
                'demo_url': project['demo_url'],
                'image_url': project['image_url'],
                'created_at': str(project['created_at']) if project['created_at'] else None
            }), 200
        else:
            return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        
        required_fields = ['title', 'description', 'technologies']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (title, description, technologies, github_url, demo_url, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['title'],
            data['description'],
            json.dumps(data['technologies']),
            data.get('github_url'),
            data.get('demo_url'),
            data.get('image_url')
        ))
        project_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Project created successfully',
            'id': project_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit a contact form"""
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
        ''', (
            data['name'],
            data['email'],
            data['subject'],
            data['message']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Message sent successfully! Thank you for reaching out.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact messages"""
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
        contacts = cursor.fetchall()
        cursor.close()
        conn.close()
        
        contacts_list = []
        for contact in contacts:
            contacts_list.append({
                'id': contact['id'],
                'name': contact['name'],
                'email': contact['email'],
                'subject': contact['subject'],
                'message': contact['message'],
                'created_at': str(contact['created_at']) if contact['created_at'] else None
            })
        
        return jsonify(contacts_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    # Return hardcoded skills (these don't change often)
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
    db_status = "connected" if get_db() else "disconnected"
    return jsonify({
        'status': 'healthy',
        'message': 'Portfolio API is running',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Mazin Sayed Portfolio API',
        'version': '2.0.0',
        'database': 'Supabase PostgreSQL',
        'endpoints': {
            'projects': '/api/projects',
            'contact': '/api/contact',
            'skills': '/api/skills',
            'health': '/api/health'
        }
    }), 200

# Initialize database on startup (for Vercel)
if __name__ != '__main__':
    if DATABASE_URL:
        init_db()

if __name__ == '__main__':
    # Local development mode
    if DATABASE_URL:
        print('Connecting to Supabase database...')
        init_db()
    else:
        print('WARNING: No DATABASE_URL found. Set it in environment variables.')
        print('Get your DATABASE_URL from: https://supabase.com')
    
    print('Starting Flask server...')
    print('API available at: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
