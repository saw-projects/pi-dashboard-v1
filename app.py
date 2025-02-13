from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

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
    cursor = db.cursor()
    
    # Get sort parameters
    sort_by = request.args.get('sort', 'date_paid')  # default sort by date
    sort_order = request.args.get('order', 'desc')   # default newest first
    search_invoice = request.args.get('invoice', '')
    filter_llc = request.args.get('llc', '')
    filter_property = request.args.get('property', '')
    
    # Base query
    query = 'SELECT *, date_paid as full_date, strftime("%m", date_paid) as month, strftime("%Y", date_paid) as year FROM receipts'
    params = []
    where_clauses = []
    
    # Add search/filter conditions
    if search_invoice:
        where_clauses.append('invoice_number LIKE ?')
        params.append(f'%{search_invoice}%')
    if filter_llc:
        where_clauses.append('llc = ?')
        params.append(filter_llc)
    if filter_property:
        where_clauses.append('property = ?')
        params.append(filter_property)
    
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    
    # Add sorting
    sort_column = {
        'date': 'full_date',
        'month': 'month',
        'year': 'year',
        'llc': 'llc',
        'property': 'property'
    }.get(sort_by, 'full_date')
    
    query += f' ORDER BY {sort_column} {sort_order.upper()}'
    
    cursor.execute(query, params)
    receipts = cursor.fetchall()
    
    # Get unique LLCs and properties for filters
    cursor.execute('SELECT DISTINCT llc FROM receipts ORDER BY llc')
    llcs = [row['llc'] for row in cursor.fetchall()]
    
    cursor.execute('SELECT DISTINCT property FROM receipts ORDER BY property')
    properties = [row['property'] for row in cursor.fetchall()]
    
    return render_template('view_receipts.html', 
                         receipts=receipts,
                         llcs=llcs,
                         properties=properties,
                         current_sort=sort_by,
                         current_order=sort_order,
                         current_invoice=search_invoice,
                         current_llc=filter_llc,
                         current_property=filter_property)

@app.route('/uploads/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_receipt/<int:receipt_id>', methods=['POST'])
def delete_receipt(receipt_id):
    db = get_db()
    # First get the receipt to find its PDF path
    cursor = db.cursor()
    cursor.execute('SELECT pdf_path FROM receipts WHERE id = ?', (receipt_id,))
    receipt = cursor.fetchone()
    
    if receipt and receipt['pdf_path']:
        # Delete the PDF file if it exists
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(receipt['pdf_path']))
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    
    # Delete the receipt from database
    cursor.execute('DELETE FROM receipts WHERE id = ?', (receipt_id,))
    db.commit()
    return redirect(url_for('view_receipts'))

@app.route('/edit_receipt/<int:receipt_id>', methods=['GET', 'POST'])
def edit_receipt(receipt_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        # Handle the form submission
        paid_to = request.form['paid_to']
        date_paid = request.form['date_paid']
        amount = request.form['amount']
        expense_type = request.form['expense_type']
        invoice_number = request.form['invoice_number']
        llc = request.form['llc']
        property_name = request.form['property']
        notes = request.form['notes']
        
        # Get the existing PDF path
        cursor.execute('SELECT pdf_path FROM receipts WHERE id = ?', (receipt_id,))
        existing_receipt = cursor.fetchone()
        existing_pdf_path = existing_receipt['pdf_path'] if existing_receipt else None
        
        # Handle PDF upload if provided
        pdf_file = request.files.get('pdf_file')
        if pdf_file and pdf_file.filename:
            # Delete old PDF if it exists
            if existing_pdf_path:
                old_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(existing_pdf_path))
                if os.path.exists(old_pdf_path):
                    os.remove(old_pdf_path)
            
            # Save new PDF
            filename = secure_filename(pdf_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f"{timestamp}_{filename}"
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            pdf_path = pdf_filename
        else:
            pdf_path = existing_pdf_path
        
        # Update the database
        cursor.execute('''
            UPDATE receipts 
            SET paid_to = ?, date_paid = ?, amount = ?, expense_type = ?, 
                invoice_number = ?, llc = ?, property = ?, notes = ?, pdf_path = ?
            WHERE id = ?
        ''', (paid_to, date_paid, amount, expense_type, invoice_number, llc, 
              property_name, notes, pdf_path, receipt_id))
        db.commit()
        return redirect(url_for('view_receipts'))
    
    # GET request - show the edit form
    cursor.execute('SELECT * FROM receipts WHERE id = ?', (receipt_id,))
    receipt = cursor.fetchone()
    if receipt:
        return render_template('edit_receipt.html', receipt=receipt)
    return redirect(url_for('view_receipts'))

@app.route('/sandpi')
def sandpi():
    return "Sandpi Dashboard - Coming Soon"

@app.route('/scraper')
def scraper():
    return "Scraper Dashboard - Coming Soon"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
