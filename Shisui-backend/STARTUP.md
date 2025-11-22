# Starting Shisui Backend

## Quick Start

### Windows
Double-click `start.bat` or run:
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

## What the Startup Script Does

1. **Checks MySQL Status** - Verifies MySQL/MariaDB is running
2. **Warns if Not Running** - Provides instructions to start MySQL
3. **Activates Virtual Environment** - Automatically activates Python venv
4. **Starts Backend** - Runs `python main.py`

## Manual Start

If you prefer to start manually:

```bash
# 1. Make sure MySQL is running (XAMPP/WAMP)

# 2. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Run the app
python main.py
```

## Troubleshooting

### MySQL Not Running

**Error:** `Can't connect to MySQL server on 'localhost:3306'`

**Solution:**
- **XAMPP:** Open XAMPP Control Panel → Start MySQL
- **WAMP:** Click WAMP icon → Start MySQL
- **Standalone:** Run `net start MySQL` (Windows) or `sudo systemctl start mysql` (Linux)

### Database Not Found

**Error:** `Unknown database 'shisui'`

**Solution:**
```sql
CREATE DATABASE shisui CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
Then import `DB/shisui.sql`

### Wrong Credentials

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:** Update `.env` file with correct credentials:
```
DB_USER=root
DB_PASSWORD=your_actual_password
```

## Production Deployment

For production, MySQL should be:
- Running as a system service (always on)
- Configured with proper credentials
- Backed up regularly
- Monitored for uptime

The app will gracefully handle database connection failures and continue running with limited functionality.
