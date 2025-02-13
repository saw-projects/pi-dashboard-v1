CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paid_to TEXT NOT NULL,
    date_paid DATE NOT NULL,
    expense_type TEXT NOT NULL,
    invoice_number TEXT,
    notes TEXT,
    llc TEXT NOT NULL,
    property TEXT NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    pdf_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
