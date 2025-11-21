# Database Specification for Shisui Student History

This document specifies the schema for the local SQL database used to track student history and interactions.

## Database Type
SQLite (local file: `shisui_history.db`)

## Schema

### 1. `sessions`
Tracks unique student sessions.
```sql
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. `interactions`
Logs every chat exchange between the student and the agents.
```sql
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_query TEXT,
    agent_response TEXT,
    agent_name TEXT, -- 'planner', 'course', 'exam'
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

### 3. `study_sessions`
Records timed study blocks.
```sql
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    topic TEXT,
    duration_minutes INTEGER,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

### 4. `exam_results`
Stores results of generated exams.
```sql
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    topic TEXT,
    score INTEGER, -- Percentage or raw score
    total_questions INTEGER,
    pdf_url TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

## Setup Script (Python)

This script should be run to initialize the database.

```python
import sqlite3
import os

DB_FILE = "shisui_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_query TEXT,
        agent_response TEXT,
        agent_name TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )
    ''')
    
    # Create study_sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        topic TEXT,
        duration_minutes INTEGER,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )
    ''')
    
    # Create exam_results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        topic TEXT,
        score INTEGER,
        total_questions INTEGER,
        pdf_url TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_FILE}")

if __name__ == "__main__":
    init_db()
```
