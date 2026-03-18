# Hosting Lexora on Render (Free Tier)

This guide explains how to host the Lexora Web Editor on [Render.com](https://render.com) for free.

## Prerequisites
1. A [GitHub](https://github.com) account.
2. A [Render](https://render.com) account (Sign up with GitHub).

## Deployment Steps

### 1. Push Code to GitHub
Ensure your code is pushed to a GitHub repository.

### 2. Create a New Web Service on Render
1. Log in to your Render Dashboard.
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` file and configure the service.
   - **Name**: `lexora-web-editor` (or your preferred name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r lexora-web-editor/requirements.txt`
   - **Start Command**: `cd lexora-web-editor/src && gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

### 3. Configure Environment Variables
In the Render dashboard for your service:
1. Go to **Environment**.
2. Add the following variable:
   - `FLASK_ENV`: `production`

### 4. Deploy
1. Click **Create Web Service**.
2. Wait for the build to complete (usually 2-3 minutes).
3. Your app will be live at `https://your-app-name.onrender.com`.

## Free Tier Notes
- **Spin-down**: Render's free tier services spin down after 15 minutes of inactivity. The first request after a spin-down will take ~30 seconds to wake up the server.
- **Port**: Render automatically provides a `$PORT` environment variable which the app is configured to use.

---
*Built with Lexora - The Future of Programming.*
