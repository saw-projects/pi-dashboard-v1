#!/bin/bash

echo "Setting up Pi Dashboard..."

# Create necessary directories
echo "Creating directories..."
mkdir -p /home/sandpi/pi-dashboard
mkdir -p /home/sandpi/pi-dashboard/uploads

# Set permissions
echo "Setting permissions..."
sudo chown sandpi:sandpi /home/sandpi/databases
chmod 755 uploads

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv /home/sandpi/pi-dashboard/venv
source /home/sandpi/pi-dashboard/venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
sqlite3 /home/sandpi/databases/receipts.db < schema.sql

echo "Setup complete! You can now run the application with:"
echo "source /home/sandpi/pi-dashboard/venv/bin/activate"
echo "python app.py"
