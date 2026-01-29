# AI Developer Portfolio Website

A modern, fully animated portfolio website for an AI Student and Web Developer, featuring a neural network background animation, smooth transitions, and a complete backend system.

## 🚀 Features

### Frontend
- **Modern Design**: Bold, cyberpunk-inspired aesthetic with animated elements
- **Neural Network Background**: Interactive particle animation that simulates neural connections
- **Smooth Animations**: Fade-in effects, hover states, and smooth scrolling
- **Typewriter Effect**: Animated code display in the hero section
- **Responsive Design**: Fully responsive layout that works on all devices
- **Interactive UI**: Hover effects, parallax scrolling, and custom cursor
- **Dynamic Content**: Projects and skills loaded from backend API

### Backend
- **RESTful API**: Complete REST API built with Flask
- **Database Integration**: SQLite database for storing projects, contacts, and skills
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for projects
- **Contact Form**: Backend handling for contact form submissions
- **CORS Enabled**: Cross-Origin Resource Sharing for frontend-backend communication

## 📁 Project Structure

```
portfolio/
├── index.html          # Main HTML file
├── styles.css          # CSS with animations and responsive design
├── script.js           # JavaScript for interactivity and API calls
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── portfolio.db        # SQLite database (created automatically)
└── README.md          # This file
```

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3 (with CSS Variables and Animations)
- Vanilla JavaScript (ES6+)
- Google Fonts (Syne & JetBrains Mono)

### Backend
- Python 3.8+
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLite (Database)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Clone or Download Files
Place all files in a single directory:
- index.html
- styles.css
- script.js
- app.py
- requirements.txt

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask flask-cors
```

### Step 3: Run the Backend Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see:
```
Initializing database...
Database initialized successfully!
Starting Flask server...
API available at: http://localhost:5000
```

### Step 4: Open the Frontend
Open `index.html` in your web browser, or serve it using a simple HTTP server:

**Option 1: Direct Open**
```
Double-click index.html
```

**Option 2: Python HTTP Server**
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`

## 🔌 API Endpoints

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get specific project
- `POST /api/projects` - Create new project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Contact
- `POST /api/contact` - Submit contact form
- `GET /api/contacts` - Get all contact messages

### Skills
- `GET /api/skills` - Get all skills
- `POST /api/skills` - Add new skill

### Health Check
- `GET /api/health` - Check API status

## 📊 Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    technologies TEXT NOT NULL,  -- JSON array
    github_url TEXT,
    demo_url TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Contacts Table
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Skills Table
```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    level INTEGER NOT NULL,  -- 0-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #0A0E27;
    --accent-color: #00F0FF;
    --accent-secondary: #FF006E;
    /* ... more colors */
}
```

### Content
1. **Personal Info**: Edit text in `index.html`
2. **Projects**: Add/edit via API or directly in database
3. **Skills**: Modify skill bars and percentages in HTML
4. **Contact Info**: Update contact details in the contact section

### Animations
- Neural network: Adjust in `script.js` `NeuralNetwork` class
- Typewriter: Modify text in `Typewriter` class
- Timings: Change CSS animation durations

## 🔐 API Usage Examples

### Create a Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Project",
    "description": "An amazing project description",
    "technologies": ["Python", "React", "MongoDB"],
    "github_url": "https://github.com/username/project"
  }'
```

### Submit Contact Form
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Project Inquiry",
    "message": "I would like to discuss a project..."
  }'
```

### Get All Projects
```bash
curl http://localhost:5000/api/projects
```

## 🌐 Deployment

### Frontend Deployment
Deploy to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

### Backend Deployment
Deploy to:
- Heroku
- PythonAnywhere
- AWS EC2
- DigitalOcean
- Google Cloud

**Note**: Update `API_BASE_URL` in `script.js` when deploying backend to production.

## 📱 Responsive Breakpoints
- Desktop: > 968px
- Tablet: 640px - 968px
- Mobile: < 640px

## ⚡ Performance Tips
1. Minify CSS and JavaScript for production
2. Optimize images before adding
3. Use CDN for fonts
4. Enable caching on server
5. Consider lazy loading for images

## 🐛 Troubleshooting

### CORS Error
If you see CORS errors, ensure:
1. Flask-CORS is installed
2. Backend is running on port 5000
3. Frontend URL is allowed

### Database Not Found
The database is created automatically on first run. If issues occur:
```bash
python -c "from app import init_db; init_db()"
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📄 License
This project is open source and available under the MIT License.

## 🤝 Contributing
Feel free to fork, modify, and use this portfolio template for your own projects!

## 📧 Contact
For questions or suggestions, use the contact form on the website or reach out directly.

## 🎓 Learning Resources
- Flask Documentation: https://flask.palletsprojects.com/
- JavaScript Animation: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- CSS Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations

---

Built with ❤️ using HTML, CSS, JavaScript, Python, and Flask
