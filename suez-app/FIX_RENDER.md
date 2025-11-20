# 🔧 Fix Your Current Render Deployment

You're getting the build error because Render needs a Dockerfile to install system dependencies like Tesseract and Poppler.

## Quick Fix (2 minutes)

### Step 1: Add Missing Files to Your GitHub Repo

Add these two new files to your repository:

**1. Create `Dockerfile`** (in root of repo):
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create temp directory for uploads
RUN mkdir -p /tmp/suez_uploads

# Expose port
EXPOSE 10000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
```

**2. Create `render.yaml`** (in root of repo):
```yaml
services:
  - type: web
    name: suez-glossop-extractor
    env: docker
    dockerfilePath: ./Dockerfile
    healthCheckPath: /
```

### Step 2: Push to GitHub

```bash
git add Dockerfile render.yaml
git commit -m "Add Dockerfile for Render deployment"
git push
```

### Step 3: Update Render Settings

1. Go to your Render dashboard
2. Click on your service
3. Go to "Settings"
4. **Delete the custom Build Command** (leave it blank)
5. **Delete the custom Start Command** (leave it blank)
6. Click "Save Changes"
7. Go to "Manual Deploy" → "Deploy latest commit"

### Step 4: Wait for Build

Render will now:
- ✅ Detect the Dockerfile
- ✅ Install Tesseract and Poppler correctly
- ✅ Build and deploy successfully
- ⏱️ Takes about 5-10 minutes

## What Changed?

**Before (didn't work):**
- Tried to use `apt-get` in build command
- Render's environment is read-only
- ❌ Failed

**After (will work):**
- Use Dockerfile to install system packages
- Render builds a complete Docker image
- ✅ Success!

## Verify It Worked

Once deployed, you should see:
```
==> Using Dockerfile
==> Building image...
==> Installing tesseract-ocr
==> Installing poppler-utils
==> Installing Python packages
==> Build succeeded!
==> Your service is live at https://your-app.onrender.com
```

## Still Having Issues?

### Check the logs:
1. Go to Render dashboard
2. Click "Logs"
3. Look for error messages

### Common issues:
- **"Dockerfile not found"**: Make sure Dockerfile is in the root directory
- **"Port binding failed"**: The Dockerfile uses port 10000 (Render's default)
- **"Module not found"**: Make sure all files are in the repo

## Alternative: Start Fresh

If you want to start over:
1. Delete the current Render service
2. Create a new one from GitHub
3. Render will auto-detect the Dockerfile
4. No need to configure anything!

## Need the Files?

I've created updated versions with Dockerfile included. Download the new package and push everything to GitHub.
