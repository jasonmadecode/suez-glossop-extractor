# Suez Glossop Weighbridge Extractor

A web application that extracts ticket data from scanned Suez Glossop weighbridge PDFs using OCR.

## Features

- 📄 Upload scanned PDF files
- 🔍 Server-side OCR (much better than browser OCR)
- 📊 Automatic data extraction (ticket numbers, dates, weights)
- 📥 Download formatted Excel spreadsheet
- 🎯 Real-time progress tracking

## Quick Deploy Options

### Option 1: Deploy to Render (Easiest - FREE)

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub (or create a repo with these files)
4. Settings:
   - **Build Command**: `apt-get update && apt-get install -y tesseract-ocr poppler-utils && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
5. Click "Create Web Service"
6. Wait 5-10 minutes for deployment

### Option 2: Deploy to Railway (FREE)

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo with these files
4. Railway auto-detects Python and deploys
5. Add build command: `apt-get update && apt-get install -y tesseract-ocr poppler-utils`
6. Your app will be live at a railway.app URL

### Option 3: Deploy to PythonAnywhere

1. Create account at https://www.pythonanywhere.com (Free tier)
2. Upload these files via "Files" tab
3. Open Bash console and run:
   ```bash
   pip install --user -r requirements.txt
   sudo apt-get install tesseract-ocr poppler-utils
   ```
4. Configure web app in "Web" tab
5. Set WSGI file to point to your app

### Option 4: Run Locally

1. Install dependencies:
   ```bash
   # Mac
   brew install tesseract poppler
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr poppler-utils
   
   # Windows
   # Download and install from:
   # https://github.com/UB-Mannheim/tesseract/wiki
   # https://blog.alivate.com.au/poppler-windows/
   ```

2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open browser to: http://localhost:5000

## System Requirements

- **Tesseract OCR** - for text recognition
- **Poppler** - for PDF to image conversion
- **Python 3.8+**

## How It Works

1. Upload your scanned Suez Glossop PDF
2. Server converts each page to high-resolution image
3. OCR extracts text from images
4. Smart parser finds ticket numbers, dates, and weights
5. Data exported to formatted Excel spreadsheet

## Troubleshooting

**Issue**: "No tickets found"
- Ensure PDF is from Suez Glossop weighbridge
- Check PDF isn't password protected
- Try rescanning at higher quality

**Issue**: "Missing dependencies"
- Install Tesseract and Poppler (see deployment steps)
- Verify with: `tesseract --version` and `pdfinfo -v`

**Issue**: Slow processing
- Normal for scanned PDFs (2-3 seconds per page)
- Server processes at higher quality than browser

## Files

```
suez-app/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface
└── README.md          # This file
```

## Support

For deployment help or issues, check:
- Render docs: https://render.com/docs
- Railway docs: https://docs.railway.app
- PythonAnywhere: https://help.pythonanywhere.com

## License

Free to use for Suez Glossop data extraction
