from flask import Flask, render_template, request, send_file, jsonify, Response
import io
import os
import pdf2image
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import openpyxl
from openpyxl.styles import Alignment
from datetime import datetime
import re
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/suez_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def enhance_image(image):
    """Enhance image for better OCR"""
    # Convert to grayscale
    image = image.convert('L')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)
    
    # Threshold to black and white
    threshold = 128
    image = image.point(lambda p: 255 if p > threshold else 0)
    
    return image

def extract_ticket_from_text(text):
    """Extract ticket data from OCR text"""
    
    # Clean up text
    text = text.replace('|', 'I').replace('`', '').replace("'", '')
    
    # Find ticket number
    ticket_match = re.search(r'(\d{4}[\s\-]?[PpBbRr][\s\-]?\d{9})', text)
    if not ticket_match:
        ticket_match = re.search(r'Ticket\s*No[:\s]*(\d{4}[\s\-]?[PpBbRr][\s\-]?\d{9})', text, re.IGNORECASE)
    
    if not ticket_match:
        return None
    
    ticket_full = ticket_match.group(1).replace(' ', '').replace('-', '').upper()
    ticket_full = re.sub(r'[BR]', 'P', ticket_full)
    ticket_no = ticket_full[-9:]
    
    # Find date
    date_match = re.search(r'Date[:\s]*(\d{1,2})[\s\-]([A-Za-z]{3})[\s\-](\d{4})', text, re.IGNORECASE)
    if not date_match:
        date_match = re.search(r'(\d{1,2})[\s\-]([A-Za-z]{3})[\s\-](202[45])', text)
    
    if not date_match:
        return None
    
    day = date_match.group(1).zfill(2)
    month = date_match.group(2)
    year = date_match.group(3)
    
    try:
        date_obj = datetime.strptime(f"{day}-{month}-{year}", "%d-%b-%Y")
    except:
        return None
    
    # Find weights
    gross_match = re.search(r'GROSS[^\d]{0,20}(\d{3,5})', text, re.IGNORECASE)
    tare_match = re.search(r'TARE[^\d]{0,20}(\d{3,5})', text, re.IGNORECASE)
    net_match = re.search(r'NET[^\d]{0,20}(\d{2,5})', text, re.IGNORECASE)
    
    if gross_match and tare_match and net_match:
        gross = int(gross_match.group(1))
        tare = int(tare_match.group(1))
        net = int(net_match.group(1))
    else:
        return None
    
    # Validate
    if net > gross or tare > gross or net <= 0:
        return None
    
    # Determine type
    waste_type = 'Flytip'
    upper_text = text.upper()
    if 'STREET' in upper_text or 'CLEAN' in upper_text or 'LITTER' in upper_text:
        waste_type = 'Street/Litter'
    elif 'BIODEGRADABLE' in upper_text or 'COMPOST' in upper_text or 'KITCHEN' in upper_text:
        waste_type = 'Compost'
    
    return {
        'ticket_no': ticket_no,
        'date': date_obj,
        'day': date_obj.strftime('%A'),
        'gross': gross,
        'tare': tare,
        'net': net,
        'type': waste_type
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    
    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    def generate():
        try:
            # Convert PDF to images
            pdf_bytes = pdf_file.read()
            images = pdf2image.convert_from_bytes(pdf_bytes, dpi=300)
            
            tickets = []
            total_pages = len(images)
            
            for page_num, image in enumerate(images, 1):
                # Enhance image
                enhanced = enhance_image(image)
                
                # Perform OCR
                text = pytesseract.image_to_string(enhanced)
                
                # Extract ticket
                ticket = extract_ticket_from_text(text)
                if ticket:
                    tickets.append(ticket)
                
                yield f"data: {json.dumps({'status': 'processing', 'page': page_num, 'total': total_pages, 'found': len(tickets)})}\n\n"
            
            if not tickets:
                yield f"data: {json.dumps({'status': 'error', 'message': 'No tickets found'})}\n\n"
                return
            
            # Sort by date
            tickets.sort(key=lambda x: x['date'])
            
            # Create Excel
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Suez Glossop Tickets"
            
            # Headers
            headers = ["Week", "Type", "Date", "Day", "IN", "OUT", "Nett", "Street/Litter", "Flytip Monthly", "Compost", "Ticket No"]
            for col, header in enumerate(headers, 1):
                ws.cell(1, col).value = header
            
            # Data
            for row_num, ticket in enumerate(tickets, 2):
                ws.cell(row_num, 1).value = None
                ws.cell(row_num, 2).value = ticket['type']
                
                date_cell = ws.cell(row_num, 3)
                date_cell.value = ticket['date']
                date_cell.number_format = 'DD/MM/YYYY'
                date_cell.alignment = Alignment(horizontal='right')
                
                ws.cell(row_num, 4).value = ticket['day']
                ws.cell(row_num, 5).value = ticket['gross']
                ws.cell(row_num, 6).value = ticket['tare']
                ws.cell(row_num, 7).value = ticket['net']
                ws.cell(row_num, 8).value = None
                ws.cell(row_num, 9).value = None
                ws.cell(row_num, 10).value = None
                
                ticket_cell = ws.cell(row_num, 11)
                ticket_cell.value = ticket['ticket_no']
                ticket_cell.alignment = Alignment(horizontal='right')
            
            # Save file
            filename = f"suez-glossop-tickets-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            wb.save(filepath)
            
            yield f"data: {json.dumps({'status': 'complete', 'tickets': len(tickets), 'filename': filename})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
