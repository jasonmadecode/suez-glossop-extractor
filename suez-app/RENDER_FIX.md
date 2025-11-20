# 🔧 FIXED: Render Deployment Instructions

## The Issue
Render's Python environment doesn't allow `apt-get` in build commands.

## ✅ Solution: Use Docker

I've added a `Dockerfile` that handles everything properly.

## Steps to Deploy on Render

1. **Add the Dockerfile to your GitHub repo**
   - Upload the new `Dockerfile` from this package
   - Commit and push to GitHub

2. **Configure Render Service**
   - Go to your Render dashboard
   - Click on your service (or create new)
   - **Important Settings:**
     - **Environment**: Select **"Docker"** (not Python!)
     - **Dockerfile Path**: `Dockerfile`
     - **Docker Build Context Directory**: `.` (root)
     - Leave build command EMPTY
     - Leave start command EMPTY (Dockerfile handles it)

3. **Deploy**
   - Click "Create Web Service" or "Manual Deploy"
   - Render will use Docker and install all dependencies correctly
   - Wait 5-10 minutes

4. **Done!**
   - Your app will be live at your Render URL
   - All OCR dependencies installed correctly

## Alternative: Manual Configuration (Without Docker)

If you prefer not to use Docker:

1. **In Render Dashboard:**
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

2. **Add Environment Variable:**
   - Key: `PYTHON_VERSION`
   - Value: `3.11.6`

3. **Contact Render Support** to request:
   - `tesseract-ocr` package
   - `poppler-utils` package
   
   (They can enable these for your service)

## Files You Need

Make sure these are in your GitHub repo:
```
✅ Dockerfile          # Handles all dependencies
✅ app.py              # Main application
✅ requirements.txt    # Python packages
✅ templates/index.html
✅ runtime.txt         # Optional, but good to have
```

## Quick Test

After deployment, visit your URL and you should see the upload interface!

## Still Having Issues?

Try **Railway** instead - it's even easier:

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Add Dockerfile (Railway auto-detects it)
5. Deploy - Done in 3 minutes!

Railway has better Docker support out of the box.
