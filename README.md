# Pi Dashboard

A lightweight Flask web application designed for Raspberry Pi Zero to manage various services including receipts, sandpi monitoring, and web scraping.

## Setup

1. Clone the repository to your Raspberry Pi:
```bash
git clone <repository-url> /home/sandpi/pi-dashboard
cd /home/sandpi/pi-dashboard
```

2. Create and set up Python virtual environment:
```bash
python3 -m venv /home/sandpi/pi-dashboard/venv
source /home/sandpi/pi-dashboard/venv/bin/activate
pip install -r requirements.txt
```

3. Initialize database and set permissions:
```bash
# Create database directory
sudo mkdir -p /home/sandpi/databases
sudo chown sandpi:sandpi /home/sandpi/databases

# Initialize database
sqlite3 /home/sandpi/databases/receipts.db < schema.sql

# Create uploads directory
mkdir -p uploads
chmod 755 uploads
```

## Running the Application

1. Start the Flask application:
```bash
source /home/sandpi/pi-dashboard/venv/bin/activate
python app.py
```

The application will be available at:
`http://<raspberry-pi-ip>:5000`

## Features

- Multi-service dashboard interface
- Receipts Management:
  - Enter receipts with PDF attachments
  - View recent receipts (last 20 entries)
  - Automatic date-based organization
- Sandpi Monitoring (coming soon)
- Web Scraper Interface (coming soon)
- PDF storage in `uploads/` directory
- SQLite database at `/home/sandpi/databases/receipts.db`

## Routes

- `/` - Main dashboard
- `/receipts` - Receipts dashboard
- `/view-receipts` - View recent entries
- `/sandpi` - Sandpi monitoring dashboard
- `/scraper` - Web scraper dashboard
