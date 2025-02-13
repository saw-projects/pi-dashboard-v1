# Receipts Dashboard

A lightweight Flask web application designed for Raspberry Pi Zero to manage receipts and expenses.

## Setup

1. Clone the repository to your Raspberry Pi:
```bash
git clone <repository-url> /home/sandpi/receipts-dashboard
cd /home/sandpi/receipts-dashboard
```

2. Install Apache and mod_wsgi:
```bash
sudo apt-get update
sudo apt-get install apache2 libapache2-mod-wsgi-py3
```

3. Install Python dependencies in the virtual environment:
```bash
source /home/sandpi/pi-dashboard/venv/bin/activate
pip install -r requirements.txt
```

4. Initialize database:
```bash
sqlite3 /home/sandpi/databases/receipts.db < schema.sql
```

## Apache Deployment

1. Remove default Apache site:
```bash
sudo a2dissite 000-default.conf
```

2. Copy the Apache configuration:
```bash
sudo cp receipts-dashboard.conf /etc/apache2/sites-available/
```

3. Enable the site and mod_wsgi:
```bash
sudo a2ensite receipts-dashboard
sudo a2enmod wsgi
```

4. Test Apache configuration:
```bash
sudo apache2ctl configtest
```

5. Restart Apache:
```bash
sudo systemctl restart apache2
```

The application will now be available at:
`http://<raspberry-pi-ip>/`

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

- View Apache logs:
  ```bash
  sudo tail -f /var/log/apache2/receipts-dashboard-error.log
  sudo tail -f /var/log/apache2/receipts-dashboard-access.log
  ```
- Restart Apache: `sudo systemctl restart apache2`
