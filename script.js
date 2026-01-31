// Configuration
// Auto-detects localhost vs production (Vercel)
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : '/api';

// Neural Network Background
class NeuralNetwork {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.container = document.getElementById('neuralNetwork');
        this.container.appendChild(this.canvas);
        
        this.nodes = [];
        this.connections = [];
        this.nodeCount = 50;
        
        this.resize();
        this.init();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    init() {
        this.nodes = [];
        for (let i = 0; i < this.nodeCount; i++) {
            this.nodes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update nodes
        this.nodes.forEach(node => {
            node.x += node.vx;
            node.y += node.vy;
            
            if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1;
        });
        
        // Draw connections
        this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.1)';
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const dx = this.nodes[i].x - this.nodes[j].x;
                const dy = this.nodes[i].y - this.nodes[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y);
                    this.ctx.lineTo(this.nodes[j].x, this.nodes[j].y);
                    this.ctx.stroke();
                }
            }
        }
        
        // Draw nodes
        this.nodes.forEach(node => {
            this.ctx.fillStyle = 'rgba(0, 240, 255, 0.6)';
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Typewriter Effect
class Typewriter {
    constructor(element) {
        this.element = element;
        this.texts = [
            'Name: Mazin Sayed\nAge: 18y\nUniversity: Galala (GU)\nFaculty: Computer Science\nSpecialization: Artificial Intelligence'
        ];
        this.textIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.type();
    }
    
    type() {
        const currentText = this.texts[this.textIndex];
        
        if (!this.isDeleting) {
            this.element.textContent = currentText.substring(0, this.charIndex + 1);
            this.charIndex++;
            
            if (this.charIndex === currentText.length) {
                setTimeout(() => this.type(), 2000);
                return;
            }
        }
        
        setTimeout(() => this.type(), this.isDeleting ? 30 : 50);
    }
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Active Navigation Link
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Navbar Scroll Effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
const menuToggle = document.getElementById('menuToggle');
const navLinksContainer = document.querySelector('.nav-links');

menuToggle?.addEventListener('click', () => {
    navLinksContainer.classList.toggle('active');
});

// Counter Animation
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.ceil(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + '+';
        }
    };
    
    updateCounter();
}

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            
            // Animate counters
            const counters = entry.target.querySelectorAll('.stat-number');
            counters.forEach(counter => {
                if (!counter.classList.contains('animated')) {
                    counter.classList.add('animated');
                    animateCounter(counter);
                }
            });
            
            // Animate skill bars
            const skillBars = entry.target.querySelectorAll('.skill-progress');
            skillBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section > .container').forEach(section => {
    observer.observe(section);
});

// Load Projects
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        const projects = await response.json();
        
        const projectsGrid = document.getElementById('projectsGrid');
        projectsGrid.innerHTML = '';
        
        projects.forEach(project => {
            const projectCard = createProjectCard(project);
            projectsGrid.appendChild(projectCard);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
        // Display sample projects if API fails
        displaySampleProjects();
    }
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    
    const techTags = project.technologies.map(tech => 
        `<span class="tech-tag">${tech}</span>`
    ).join('');
    
    card.innerHTML = `
        <div class="project-image">
            <span style="font-size: 3rem;">🚀</span>
        </div>
        <div class="project-content">
            <h3 class="project-title">${project.title}</h3>
            <p class="project-description">${project.description}</p>
            <div class="project-tech">
                ${techTags}
            </div>
            ${project.github_url ? `<a href="${project.github_url}" class="project-link" target="_blank">View Project →</a>` : ''}
        </div>
    `;
    
    return card;
}

function displaySampleProjects() {
    const sampleProjects = [
        {
            title: 'AI Image Recognition',
            description: 'Deep learning model for image classification using CNN architecture. Achieved 95% accuracy on test dataset.',
            technologies: ['Python', 'TensorFlow', 'OpenCV', 'Flask'],
            github_url: '#'
        },
        {
            title: 'Real-time Chat Application',
            description: 'Full-stack chat app with WebSocket support, user authentication, and message encryption.',
            technologies: ['React', 'Node.js', 'Socket.io', 'MongoDB'],
            github_url: '#'
        },
        {
            title: 'Predictive Analytics Dashboard',
            description: 'Interactive dashboard for data visualization and predictive modeling using machine learning algorithms.',
            technologies: ['Python', 'Pandas', 'Plotly', 'Scikit-learn'],
            github_url: '#'
        },
        {
            title: 'E-commerce Platform',
            description: 'Modern e-commerce solution with payment integration, inventory management, and admin dashboard.',
            technologies: ['Vue.js', 'Django', 'PostgreSQL', 'Stripe'],
            github_url: '#'
        },
        {
            title: 'NLP Sentiment Analysis',
            description: 'Natural language processing tool for analyzing sentiment in social media posts and reviews.',
            technologies: ['Python', 'NLTK', 'Transformers', 'FastAPI'],
            github_url: '#'
        },
        {
            title: 'Smart Home Automation',
            description: 'IoT-based home automation system with voice control and mobile app integration.',
            technologies: ['Python', 'React Native', 'MQTT', 'Raspberry Pi'],
            github_url: '#'
        }
    ];
    
    const projectsGrid = document.getElementById('projectsGrid');
    projectsGrid.innerHTML = '';
    
    sampleProjects.forEach(project => {
        const projectCard = createProjectCard(project);
        projectsGrid.appendChild(projectCard);
    });
}

// Contact Form Submission
const contactForm = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');

contactForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = contactForm.querySelector('.btn-submit');
    submitBtn.classList.add('loading');
    formStatus.style.display = 'none';
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        subject: document.getElementById('subject').value,
        message: document.getElementById('message').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            formStatus.textContent = result.message || 'Message sent successfully!';
            formStatus.className = 'form-status success';
            contactForm.reset();
        } else {
            throw new Error(result.error || 'Failed to send message');
        }
    } catch (error) {
        console.error('Error:', error);
        formStatus.textContent = 'Failed to send message. Please try again.';
        formStatus.className = 'form-status error';
    } finally {
        submitBtn.classList.remove('loading');
        formStatus.style.display = 'block';
        
        setTimeout(() => {
            formStatus.style.display = 'none';
        }, 5000);
    }
});

// Floating Labels
const formInputs = document.querySelectorAll('.form-input');
formInputs.forEach(input => {
    input.setAttribute('placeholder', ' ');
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Initialize neural network background
    new NeuralNetwork();
    
    // Initialize typewriter effect
    const typewriterElement = document.getElementById('typewriter');
    if (typewriterElement) {
        new Typewriter(typewriterElement);
    }
    
    // Load projects
    loadProjects();
    
    // Animate elements on load
    setTimeout(() => {
        document.querySelector('.hero-content')?.classList.add('fade-in-up');
    }, 100);
});

// Parallax Effect
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero-visual');
    
    parallaxElements.forEach(element => {
        const speed = 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Cursor Effect (Optional Enhancement)
const cursor = document.createElement('div');
cursor.className = 'custom-cursor';
document.body.appendChild(cursor);

document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
});

// Add custom cursor styles
const style = document.createElement('style');
style.textContent = `
    .custom-cursor {
        width: 20px;
        height: 20px;
        border: 2px solid var(--accent-color);
        border-radius: 50%;
        position: fixed;
        pointer-events: none;
        z-index: 9999;
        transition: 0.1s;
        display: none;
    }
    
    @media (min-width: 1024px) {
        .custom-cursor {
            display: block;
        }
    }
`;
document.head.appendChild(style);

// Console Easter Egg
console.log('%c👨‍💻 Welcome to my Portfolio!', 'color: #00F0FF; font-size: 20px; font-weight: bold;');
console.log('%cInterested in the code? Check out the GitHub repo!', 'color: #B8C5D6; font-size: 14px;');
console.log('%c🚀 Built with passion and lots of coffee', 'color: #FF006E; font-size: 12px;');
