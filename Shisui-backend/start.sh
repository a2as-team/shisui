#!/bin/bash
# Shisui Backend Startup Script (Linux/Mac)
# This script checks if MySQL is running before starting the app

echo "============================================"
echo "Shisui Backend Startup"
echo "============================================"
echo ""

# Check if MySQL is running
echo "[1/2] Checking MySQL service..."
if pgrep -x mysqld > /dev/null || pgrep -x mariadbd > /dev/null; then
    echo "[OK] MySQL is running"
else
    echo "[WARNING] MySQL is not running!"
    echo ""
    echo "Please start MySQL:"
    echo "  - sudo systemctl start mysql"
    echo "  - or sudo service mysql start"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
fi

echo ""
echo "[2/2] Starting Shisui Backend..."
echo ""

# Activate virtual environment and run
source venv/bin/activate
python main.py
