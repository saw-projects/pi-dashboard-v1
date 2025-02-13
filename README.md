# Receipts Dashboard

A lightweight Flask web application designed for Raspberry Pi Zero to manage receipts and expenses.

## Setup

1. Clone the repository to your Raspberry Pi:
```bash
git clone <repository-url> /home/sandpi/receipts-dashboard
cd /home/sandpi/receipts-dashboard
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
sqlite3 /home/sandpi/databases/receipts.db < schema.sql
```

## Deployment

1. Copy the service file to systemd:
```bash
sudo cp receipts-dashboard.service /etc/systemd/system/
```

2. Start and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start receipts-dashboard
sudo systemctl enable receipts-dashboard
```

3. Check service status:
```bash
sudo systemctl status receipts-dashboard
```

The application will now:
- Start automatically on boot
- Restart if it crashes
- Run on port 5000
- Be accessible at `http://<raspberry-pi-ip>:5000`

## Features

- Simple web interface for entering receipts with PDF attachments
- View recent receipts (last 20 entries)
- Automatic date-based organization
- Minimal resource usage for Raspberry Pi Zero
- PDF storage in `uploads/` directory
- SQLite database at `/home/sandpi/databases/receipts.db`

## Routes

- `/` - Main dashboard
- `/receipts` - Enter new receipt
- `/view-receipts` - View recent entries
- `/sandpi` - Sandpi dashboard (coming soon)
- `/scraper` - Scraper dashboard (coming soon)

## Maintenance

- View logs: `sudo journalctl -u receipts-dashboard`
- Restart service: `sudo systemctl restart receipts-dashboard`
- Stop service: `sudo systemctl stop receipts-dashboard`
