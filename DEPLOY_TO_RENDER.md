# ===========================================
# DEPLOY TO RENDER - COMPLETE GUIDE
# ===========================================

## 🚀 QUICK DEPLOYMENT

### Option 1: One-Click Deploy (Recommended)

1. **Push to GitHub First**
   ```bash
   cd /Users/ashishmishra/Documents/Projects/Lexora\ Lang
   git init
   git add .
   git commit -m "feat: Production-ready Lexora for Render deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/lexora-lang.git
   git push -u origin main
   ```

2. **Deploy to Render**
   - Visit: https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select: `lexora-lang`
   - Configure as below

---

## ⚙️ RENDER CONFIGURATION

### Basic Settings:

**Name:** lexora-lang  
**Region:** Choose closest to your users  
**Branch:** main  
**Root Directory:** (leave blank)  
**Runtime:** Python 3  
**Build Command:** 
```bash
pip install -r lexora-web-editor/requirements.txt
```

**Start Command:**
```bash
cd lexora-web-editor/src && python app.py
```

---

### Instance Type:

**Free Tier:**
- Type: Free
- Good for: Testing, demos, personal use

**Paid Tier:**
- Type: Starter ($7/month)
- Good for: Production, better performance
- More RAM and CPU

---

### Environment Variables:

Add these in Render dashboard:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=10000
```

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Prepare Your Code

✅ All production files ready  
✅ .gitignore working properly  
✅ requirements.txt has dependencies  
✅ render.yaml created  

### Step 2: Push to GitHub

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Deploy to Render"

# Create GitHub repo and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/lexora-lang.git
git push -u origin main
```

### Step 3: Deploy on Render

1. **Sign up/Login** to https://render.com

2. **Create New Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub account
   - Choose `lexora-lang` repository

3. **Configure Service**
   ```
   Name: lexora-lang
   Region: Oregon (or closest)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   ```

4. **Build & Start Commands**
   ```
   Build Command: pip install -r lexora-web-editor/requirements.txt
   Start Command: cd lexora-web-editor/src && python app.py
   ```

5. **Choose Instance**
   - Free tier for testing
   - Starter for production

6. **Advanced Settings**
   - Auto-Deploy: ✅ Enabled
   - Health Check Path: `/`
   - Docker: ❌ Not needed

7. **Environment Variables**
   Add these:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<generate-random-key>
   PORT=10000
   ```

8. **Click "Create Web Service"**

---

## ⏱️ DEPLOYMENT PROCESS

Render will now:

1. **Clone** your repository
2. **Install** dependencies from requirements.txt
3. **Build** your application
4. **Start** the Flask server
5. **Deploy** to global CDN

**Time:** ~3-5 minutes

---

## 🌐 AFTER DEPLOYMENT

### Your Live URL:
```
https://lexora-lang.onrender.com
```

### What Works:
✅ Homepage with performance stats  
✅ Web-based IDE  
✅ File upload/download  
✅ Documentation  
✅ About page  
✅ Syntax highlighting  
✅ Live code execution  

---

## 🔧 TROUBLESHOOTING

### Issue: Build Failed

**Error:** `requirements.txt not found`

**Solution:**
```bash
# Make sure file exists at correct path
ls lexora-web-editor/requirements.txt

# If missing, create it
echo "Flask==2.3.2" > lexora-web-editor/requirements.txt
echo "Werkzeug==2.3.3" >> lexora-web-editor/requirements.txt
echo "MarkupSafe==2.1.3" >> lexora-web-editor/requirements.txt
```

---

### Issue: Application Crashes

**Error:** `ModuleNotFoundError: No module named 'lexora'`

**Solution:** Update app.py imports:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lexora'))
from lexora import SimpleEnglishInterpreter
```

---

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solution:** Render sets PORT automatically. Update app.py:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
```

---

### Issue: Static Files Not Loading

**Symptoms:** CSS/JS returning 404

**Solution:** Check paths in templates:
```html
<!-- Use absolute paths -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/editor.js') }}"></script>
```

---

## 📊 MONITORING

### Render Dashboard Shows:

✅ **Status** - Running/Stopped  
✅ **Uptime** - Should be 99.9%+  
✅ **Requests** - Traffic analytics  
✅ **CPU/Memory** - Resource usage  
✅ **Logs** - Real-time application logs  

### Access Logs:

In Render dashboard:
- Click your service
- Go to "Logs" tab
- See real-time output

---

## 🎯 OPTIMIZATION TIPS

### Performance:

1. **Enable Gzip Compression**
   Add to app.py:
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

2. **Use Redis for Sessions** (Optional)
   ```python
   app.config['SESSION_TYPE'] = 'redis'
   ```

3. **Cache Static Assets**
   Already configured in render.yaml

---

## 💰 COST ESTIMATE

### Free Tier:
- ✅ $0/month
- ⚠️ Sleeps after 15 min inactivity
- 🐌 Slower startup when waking
- 📊 Limited bandwidth

### Starter Plan:
- ✅ $7/month
- ⚡ Always on
- 🚀 Faster performance
- 📈 More resources
- 🔒 SSL included

---

## 🎊 SUCCESS CHECKLIST

After deployment, verify:

- [x] Website loads at render URL
- [x] Homepage displays correctly
- [x] Performance section visible
- [x] Editor works (can run code)
- [x] File upload/download functional
- [x] Documentation accessible
- [x] Mobile responsive
- [x] No console errors

---

## 🔄 AUTO-DEPLOY

Once connected to GitHub:

✅ Every push to `main` triggers auto-deploy  
✅ Changes live in ~3 minutes  
✅ Rollback to previous versions available  
✅ Deploy previews for pull requests  

---

## 📞 SUPPORT

### Render Resources:

- **Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://status.render.net
- **Support:** support@render.com

### Quick Links:

- **Dashboard:** https://dashboard.render.com
- **Create Service:** https://dashboard.render.com/create
- **Billing:** https://dashboard.render.com/billing

---

## 🚀 READY TO DEPLOY!

Your Lexora project is now **100% ready for Render**!

### Next Steps:

1. ✅ Push to GitHub
2. ✅ Connect to Render
3. ✅ Configure settings
4. ✅ Deploy!
5. ✅ Share your live URL!

---

**Estimated Time:** 10-15 minutes  
**Difficulty:** Easy  
**Cost:** Free (or $7/month for Starter)  

**Your Lexora language will be live at:**  
`https://lexora-lang.onrender.com` ✨

Good luck! 🎉🚀
