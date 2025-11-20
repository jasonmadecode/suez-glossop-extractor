# 🚀 Quick Start Guide - Deploy in 5 Minutes!

## Easiest Option: Render (100% Free)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub (recommended) or email

2. **Push Code to GitHub**
   - Create a new GitHub repository
   - Upload all the suez-app files to your repo
   - Make sure Dockerfile, render.yaml, and all other files are included

3. **Create New Web Service on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the Dockerfile!

4. **That's it!**
   - Render automatically detects the Dockerfile
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Your app will be live at: `https://suez-glossop-extractor.onrender.com`

**Important:** Don't add a custom build command - Render will use the Dockerfile automatically!

## Alternative: Railway (Also Free!)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add these environment variables in Settings:
   ```
   NIXPACKS_BUILD_CMD=apt-get update && apt-get install -y tesseract-ocr poppler-utils
   ```
6. Railway auto-deploys! Live in 3-5 minutes.

## Test Locally First (Optional)

```bash
# Extract the files
tar -xzf suez-app.tar.gz
cd suez-app

# Install system dependencies
# Mac:
brew install tesseract poppler

# Ubuntu/Linux:
sudo apt-get install tesseract-ocr poppler-utils

# Install Python packages
pip install -r requirements.txt

# Run the app
python app.py

# Open browser to: http://localhost:5000
```

## Usage

1. Open your deployed URL
2. Drop your Suez Glossop PDF
3. Click "Process PDF"
4. Watch real-time progress
5. Download Excel when complete!

## Troubleshooting

**Build fails on Render/Railway?**
- Make sure build command includes: `apt-get install -y tesseract-ocr poppler-utils`
- Check logs for specific error

**App crashes?**
- Check if Python version is 3.8+ (set in runtime.txt)
- Verify all files uploaded correctly

**No tickets found?**
- PDF must be Suez Glossop format
- Check PDF isn't corrupted
- Try rescanning at higher quality

## Files Included

```
suez-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies  
├── Procfile           # Deployment config
├── runtime.txt        # Python version
├── README.md          # Full documentation
├── QUICKSTART.md      # This file
└── templates/
    └── index.html     # Web interface
```

## Need Help?

- Check logs in Render/Railway dashboard
- Make sure Tesseract and Poppler are installed
- Verify PDF is not password-protected

## What's Next?

Once deployed, bookmark your URL and use it anytime to extract tickets from scanned PDFs!

Your remote app will:
- ✅ Process scanned PDFs with high-quality OCR
- ✅ Extract all ticket data automatically
- ✅ Generate formatted Excel files
- ✅ Work from any device with internet
- ✅ Handle multiple PDFs
- ✅ Run 24/7 on the cloud

**Free tier limits:**
- Render: 750 hours/month (always on!)
- Railway: $5 credit/month (plenty for personal use)
