# 🌐 LEXORA WEB EDITOR - PRODUCTION DEPLOYMENT GUIDE

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [Security](#security)
7. [Performance](#performance)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 OVERVIEW

### What is Lexora Web Editor?

The Lexora Web Editor is a **production-ready, browser-based IDE** for the Lexora programming language. It provides:

- ✅ Real-time code execution
- ✅ File upload/download (.lx files)
- ✅ Syntax highlighting (CodeMirror)
- ✅ Interactive documentation
- ✅ Responsive, modern UI
- ✅ Cross-platform compatibility

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Server runtime |
| **Framework** | Flask 2.3+ | Web server |
| **Interpreter** | Lexora 1.0 | Code execution |
| **Frontend** | HTML5/CSS3/JS | User interface |
| **Editor** | CodeMirror 5 | Code editing |
| **Icons** | Font Awesome 6 | UI icons |

---

## 📁 PROJECT STRUCTURE

### Production Directory Layout

```
lexora-web-editor/
├── src/                          # Source code directory
│   ├── app.py                    # Flask application entry point
│   ├── lexora/                   # Lexora interpreter package
│   │   ├── __init__.py          # Package initialization
│   │   └── lexora.py            # Main interpreter (66KB)
│   ├── static/                   # Static assets
│   │   ├── css/                 # Stylesheets
│   │   │   └── style.css        # Main stylesheet (production-optimized)
│   │   └── js/                  # JavaScript files
│   │       └── editor.js        # Editor functionality
│   └── templates/                # HTML templates
│       ├── base.html            # Base template with navigation
│       ├── index.html           # Landing page
│       ├── editor.html          # Web IDE
│       ├── docs.html            # Documentation
│       └── about.html           # Project information
├── tests/                        # Test suite
│   └── test_lexora.py           # Unit tests
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
└── README.md                     # This file
```

### Files NOT in Production (GitIgnored)

```
❌ .env/               - Virtual environment
❌ __pycache__/        - Python bytecode
❌ *.egg-info/         - Package metadata
❌ build/              - Build artifacts
❌ dist/               - Distribution packages
❌ *.log               - Log files
❌ output.txt          - Test output
❌ test_*.lx           - Test scripts
❌ .gitignore          - Git configuration
❌ *_GUIDE.md          - Development guides
```

---

## 🔧 INSTALLATION

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

**Optional (Production):**
- Gunicorn (WSGI HTTP server)
- Nginx (Reverse proxy)
- SSL certificate (HTTPS)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/lexora-lang.git
cd lexora-lang/lexora-web-editor
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `Flask==2.3.2` - Web framework
- `Werkzeug==2.3.3` - WSGI utilities
- `MarkupSafe==2.1.3` - Template safety

### Step 4: Verify Installation

```bash
# Check Flask version
flask --version

# Should show: Flask 2.3.x
```

---

## ⚙️ CONFIGURATION

### Environment Variables

Create `.env` file in root directory:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Server Configuration
PORT=5000
HOST=127.0.0.1

# Optional: Production Settings
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
MAX_UPLOAD_SIZE=10MB
```

### Security Best Practices

1. **Never commit `.env` file**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Generate secure SECRET_KEY**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

3. **Set proper file permissions**
   ```bash
   chmod 600 .env
   chmod 755 src/
   ```

---

## 🚀 DEPLOYMENT

### Option 1: Development Server (Local Testing)

```bash
cd lexora-web-editor/src
python app.py
```

**Access:** http://localhost:5001

**Use Case:** Development and testing only

---

### Option 2: Production with Gunicorn (Recommended)

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Start Production Server

```bash
cd lexora-web-editor/src
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Parameters:**
- `-w 4` - 4 worker processes
- `-b 0.0.0.0:5000` - Bind to all interfaces on port 5000
- `app:app` - Flask application object

#### As System Service (systemd)

Create `/etc/systemd/system/lexora-editor.service`:

```ini
[Unit]
Description=Lexora Web Editor
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/lexora-web-editor/src
ExecStart=/var/www/lexora-web-editor/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable lexora-editor
sudo systemctl start lexora-editor
sudo systemctl status lexora-editor
```

---

### Option 3: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir gunicorn flask

# Copy application
COPY src/ ./src/

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
```

#### Build and Run

```bash
docker build -t lexora-editor .
docker run -p 5000:5000 lexora-editor
```

---

### Option 4: Cloud Platform Deployment

#### Heroku

1. **Create `Procfile`:**
   ```
   web: gunicorn -w 4 src.app:app
   ```

2. **Deploy:**
   ```bash
   heroku create lexora-editor
   git push heroku main
   heroku ps:scale web=1
   ```

#### Vercel / Netlify

Use `vercel.json`:
```json
{
  "version": 2,
  "builds": [{
    "src": "src/app.py",
    "use": "@vercel/python"
  }],
  "routes": [{
    "src": "/(.*)",
    "dest": "src/app.py"
  }]
}
```

---

## 🔒 SECURITY

### Production Checklist

✅ **Disable Debug Mode**
```python
# In app.py or .env
FLASK_DEBUG=False
```

✅ **Use HTTPS**
- Obtain SSL certificate (Let's Encrypt free)
- Configure reverse proxy (Nginx/Apache)

✅ **Rate Limiting**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/execute", methods=["POST"])
@limiter.limit("10 per minute")
def execute():
    ...
```

✅ **Input Validation**
```python
@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    code = data['code']
    if len(code) > 10000:  # 10KB limit
        return jsonify({"error": "Code too large"}), 413
```

✅ **CORS Configuration**
```python
from flask_cors import CORS
CORS(app, resources={r"/execute": {"origins": "https://lexora.dev"}})
```

✅ **Security Headers**
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## ⚡ PERFORMANCE

### Optimization Strategies

#### 1. **Enable Caching**

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/docs')
@cache.cached(timeout=300)  # Cache for 5 minutes
def docs():
    return render_template('docs.html')
```

#### 2. **Compress Static Assets**

```bash
# Install compression tools
npm install -g uglify-js clean-css-cli

# Minify CSS
cleancss -o src/static/css/style.min.css src/static/css/style.css

# Minify JS
uglifyjs src/static/js/editor.js -o src/static/js/editor.min.js
```

#### 3. **Enable Gzip Compression**

**Nginx Configuration:**
```nginx
gzip on;
gzip_types text/css application/javascript text/plain;
gzip_min_length 1000;
```

#### 4. **Database for Sessions** (If needed)

```python
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
Session(app)
```

#### 5. **Load Balancing** (High Traffic)

```bash
# Multiple Gunicorn workers
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# With Nginx load balancer
upstream lexora {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}
```

---

## 📊 MONITORING

### Logging Setup

#### Application Logs

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler('logs/lexora.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.before_request
def log_request():
    app.logger.info(f'{request.method} {request.path}')
```

#### Error Tracking

```python
import sys
import traceback

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f'Error: {str(e)}')
    app.logger.error(traceback.format_exc())
    return jsonify({"error": "Internal server error"}), 500
```

### Metrics to Monitor

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Response Time | New Relic | > 500ms |
| Error Rate | Sentry | > 1% |
| CPU Usage | htop | > 80% |
| Memory Usage | free -m | > 90% |
| Disk Space | df -h | > 85% |
| Active Users | Google Analytics | - |

---

## 🐛 TROUBLESHOOTING

### Common Issues

#### Issue 1: Port Already in Use

**Error:**
```
Address already in use: PORT 5000
```

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
gunicorn -b 0.0.0.0:8080 app:app
```

---

#### Issue 2: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'lexora'
```

**Solution:**
```bash
# Ensure you're in correct directory
cd lexora-web-editor/src

# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install as package
pip install -e .
```

---

#### Issue 3: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Fix file permissions
chmod -R 755 /var/www/lexora-web-editor

# Fix ownership
chown -R www-data:www-data /var/www/lexora-web-editor
```

---

#### Issue 4: Static Files Not Loading

**Symptoms:**
- CSS/JS files return 404
- Page looks unstyled

**Solution:**
```python
# Ensure static_url_path is correct
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Check file permissions
chmod 644 src/static/*
```

---

### Health Check Endpoint

Add to `app.py`:

```python
@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time()
    }), 200
```

**Test:**
```bash
curl https://lexora.dev/health
```

---

## 📈 SCALING

### Horizontal Scaling

1. **Multiple Instances**
   ```bash
   # Run multiple instances behind Nginx
   gunicorn -b 127.0.0.1:5001 app:app
   gunicorn -b 127.0.0.1:5002 app:app
   gunicorn -b 127.0.0.1:5003 app:app
   ```

2. **Load Balancer Configuration**
   ```nginx
   upstream lexora_app {
       least_conn;
       server 127.0.0.1:5001;
       server 127.0.0.1:5002;
       server 127.0.0.1:5003;
   }
   
   server {
       location / {
           proxy_pass http://lexora_app;
       }
   }
   ```

### Vertical Scaling

- Increase Gunicorn workers: `-w 8`
- Increase worker threads: `--threads 4`
- Upgrade server RAM/CPU
- Use faster database (Redis for sessions)

---

## 🎯 PRODUCTION CHECKLIST

Before deploying to production:

### Pre-Deployment

- [ ] All tests passing (`pytest tests/`)
- [ ] Debug mode disabled
- [ ] Secret keys configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Environment variables set
- [ ] SSL certificate installed
- [ ] Firewall rules configured

### Post-Deployment

- [ ] Health check passes
- [ ] HTTPS redirect working
- [ ] Error pages customized
- [ ] Logging configured
- [ ] Monitoring active
- [ ] Backups scheduled
- [ ] Rate limiting enabled
- [ ] CORS configured

### Ongoing Maintenance

- [ ] Weekly dependency updates
- [ ] Monthly security audits
- [ ] Quarterly performance reviews
- [ ] Daily log rotation
- [ ] Real-time monitoring alerts

---

## 📞 SUPPORT

### Contact

- **Email:** support@lexora.dev
- **GitHub Issues:** https://github.com/yourusername/lexora-lang/issues
- **Discord:** https://discord.gg/lexora
- **Twitter:** @LexoraLang

### Resources

- **Documentation:** https://lexora.dev/docs
- **API Reference:** https://lexora.dev/api
- **Community Forum:** https://forum.lexora.dev
- **Status Page:** https://status.lexora.dev

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-14  
**License:** MIT  
**Maintainer:** Ashish Mishra
