from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/sandpi/pi-dashboard/uploads'
DATABASE = '/home/sandpi/databases/receipts.db'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receipts', methods=['GET', 'POST'])
def receipts():
    if request.method == 'POST':
        # Get form data
        paid_to = request.form['paid_to']
        date_paid = request.form['date_paid']
        amount = float(request.form['amount'])
        expense_type = request.form['expense_type']
        invoice_number = request.form['invoice_number']
        notes = request.form['notes']
        llc = request.form['llc']
        property_name = request.form['property']
        
        # Parse date to get year and month
        date_obj = datetime.strptime(date_paid, '%Y-%m-%d')
        year = date_obj.year
        month = date_obj.month
        
        # Handle PDF upload
        pdf_file = request.files.get('pdf_file')
        pdf_path = None
        if pdf_file and pdf_file.filename:
            filename = f"{date_paid}_{paid_to}_{invoice_number}.pdf".replace(' ', '_')
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(pdf_path)
        
        # Save to database
        db = get_db()
        db.execute('''
            INSERT INTO receipts 
            (paid_to, date_paid, amount, expense_type, invoice_number, notes, llc, property, year, month, pdf_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (paid_to, date_paid, amount, expense_type, invoice_number, notes, llc, property_name, year, month, pdf_path))
        db.commit()
        
        return redirect(url_for('view_receipts'))
    
    return render_template('receipts.html', current_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/view-receipts')
def view_receipts():
    db = get_db()
    receipts = db.execute('''
        SELECT date_paid, paid_to, amount, expense_type, invoice_number, 
               llc, property, notes, pdf_path
        FROM receipts 
        ORDER BY date_paid DESC, id DESC 
        LIMIT 20
    ''').fetchall()
    return render_template('view_receipts.html', receipts=receipts)

@app.route('/uploads/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/sandpi')
def sandpi():
    return "Sandpi Dashboard - Coming Soon"

@app.route('/scraper')
def scraper():
    return "Scraper Dashboard - Coming Soon"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
