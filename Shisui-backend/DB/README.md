# Shisui Database Setup

## MySQL Database Configuration

Shisui uses MySQL/MariaDB for storing student data, interactions, study sessions, and exam results.

## Prerequisites

- MySQL Server or MariaDB installed (XAMPP, WAMP, or standalone)
- MySQL server running on `localhost:3306`

## Setup Instructions

### 1. Create the Database

Open phpMyAdmin or MySQL command line and run:

```sql
CREATE DATABASE shisui CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 2. Import the Schema

Import the `shisui.sql` file located in this directory:

**Using phpMyAdmin:**
1. Select the `shisui` database
2. Click "Import" tab
3. Choose `shisui.sql` file
4. Click "Go"

**Using MySQL command line:**
```bash
mysql -u root -p shisui < shisui.sql
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` in the backend root directory and update the database credentials:

```bash
# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=shisui
DB_USER=root
DB_PASSWORD=your_password_here
```

### 4. Install Python Dependencies

```bash
pip install mysql-connector-python
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 5. Test the Connection

Run the database test:

```bash
python tests/test_database.py
```

## Database Schema

### Tables

#### `sessions`
- `session_id` (VARCHAR 36, PRIMARY KEY) - Unique session identifier
- `created_at` (TIMESTAMP) - When session was created
- `last_active` (TIMESTAMP) - Last activity timestamp

#### `interactions`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `session_id` (VARCHAR 36, FOREIGN KEY)
- `timestamp` (TIMESTAMP)
- `user_query` (TEXT) - Student's question
- `agent_response` (TEXT) - Agent's response
- `agent_name` (TEXT) - Which agent responded

#### `study_sessions`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `session_id` (VARCHAR 36, FOREIGN KEY)
- `topic` (TEXT) - Study topic
- `duration_minutes` (INT) - Planned duration
- `start_time` (TIMESTAMP)
- `completed` (BOOLEAN) - Whether session was completed

#### `exam_results`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `session_id` (VARCHAR 36, FOREIGN KEY)
- `topic` (TEXT) - Exam topic
- `score` (INT) - Score achieved
- `total_questions` (INT) - Total questions
- `pdf_url` (TEXT) - Link to generated PDF report
- `timestamp` (TIMESTAMP)

## Seeding Test Data

To populate the database with fake student data for testing:

```bash
# Seed single session
python tests/test_database.py

# Seed multiple student sessions
python tests/test_database.py --seed-multiple
```

## Troubleshooting

### Connection Errors

**Error:** `Can't connect to MySQL server`
- **Solution:** Make sure MySQL/MariaDB is running
- Check XAMPP/WAMP control panel

**Error:** `Access denied for user 'root'@'localhost'`
- **Solution:** Update `DB_PASSWORD` in `.env` with correct password

**Error:** `Unknown database 'shisui'`
- **Solution:** Create the database first (see step 1)

### Missing Tables

**Error:** `Table 'shisui.sessions' doesn't exist`
- **Solution:** Import the `shisui.sql` schema file (see step 2)

## Migration from SQLite

If you were previously using SQLite, the data is not automatically migrated. You can:

1. Export data from SQLite
2. Import into MySQL using custom migration script
3. Or start fresh with the new MySQL database

## Performance Tips

- Indexes are already created on `session_id` columns for fast lookups
- Consider adding indexes on `timestamp` if querying by date frequently
- Use connection pooling for production deployments

## Security Notes

- Never commit `.env` file with real credentials
- Use strong passwords for production databases
- Consider using environment-specific databases (dev, staging, prod)
- Regularly backup your database
