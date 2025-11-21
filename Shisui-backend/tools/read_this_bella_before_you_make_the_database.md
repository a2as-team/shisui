#  Database Specification for Shisui Student History and i swear if you say you dont get this one like utakiwa unanipima atp 

> **Purpose**: This document provides a complete guide to building the SQLite database that tracks student learning history, interactions, study sessions, and exam results for the Shisui Learning Assistant.

---

## Database Technology

**Database Type**: **SQLite3**

- **File-based**: No server required, just a single file (`shisui_history.db`)
- **Embedded**: Runs directly in the Python application
- **Zero Configuration**: No installation or setup needed
- **ACID Compliant**: Ensures data integrity and reliability
- **Cross-Platform**: Works on Windows, Mac, and Linux

**Storage Location**: `Shisui-backend/shisui_history.db`

---

##  Database Schema (4 Tables)

### 1️ `sessions` Table
**Purpose**: Tracks unique student sessions (like user accounts)

```sql
CREATE TABLE IF NOT EXISTS sessions (
    -- Unique identifier for each student session (UUID from frontend)
    session_id TEXT PRIMARY KEY,
    
    -- When this session was first created
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Last time this student was active (updated on every interaction)
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Example Data**:
| session_id | created_at | last_active |
|------------|------------|-------------|
| `abc-123-def` | `2025-01-15 10:30:00` | `2025-01-15 11:45:00` |

**Use Case**: When a user opens Shisui, a session is created. This acts as their "account" for tracking all activity.

---

### 2️ `interactions` Table
**Purpose**: Logs every chat exchange between student and AI agents

```sql
CREATE TABLE IF NOT EXISTS interactions (
    -- Auto-incrementing unique ID for each interaction
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Links to the sessions table (which student this belongs to)
    session_id TEXT,
    
    -- When this interaction happened
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- What the student asked (e.g., "Explain photosynthesis")
    user_query TEXT,
    
    -- What the AI agent responded
    agent_response TEXT,
    
    -- Which agent answered: 'planner', 'course', or 'exam'
    agent_name TEXT,
    
    -- Foreign key constraint: ensures session exists before logging interaction
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

**Example Data**:
| id | session_id | timestamp | user_query | agent_response | agent_name |
|----|------------|-----------|------------|----------------|------------|
| 1 | `abc-123` | `2025-01-15 10:35:00` | "Explain Newton's laws" | "Newton's first law states..." | `course` |

**Use Case**: Every Q&A is logged here. This builds the student's learning history and enables context-aware responses.

---

### 3️`study_sessions` Table
**Purpose**: Records timed study blocks (Pomodoro-style timers tho yall can remove this if it isnt necessary later)

```sql
CREATE TABLE IF NOT EXISTS study_sessions (
    -- Auto-incrementing unique ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Links to the sessions table
    session_id TEXT,
    
    -- What subject/topic they're studying (e.g., "Calculus")
    topic TEXT,
    
    -- How long the timer was set for (in minutes)
    duration_minutes INTEGER,
    
    -- When the study session started
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Did they complete the timer? (TRUE/FALSE)
    completed BOOLEAN DEFAULT FALSE,
    
    -- Foreign key constraint
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

**Example Data**:
| id | session_id | topic | duration_minutes | start_time | completed |
|----|------------|-------|------------------|------------|-----------|
| 1 | `abc-123` | "Biology" | 25 | `2025-01-15 11:00:00` | `TRUE` |

**Use Case**: When a student sets a 25-minute study timer for "Biology", it's logged here. Later, Shisui can analyze study patterns and habits.

---

### 4️ `exam_results` Table
**Purpose**: Stores test scores and performance data

```sql
CREATE TABLE IF NOT EXISTS exam_results (
    -- Auto-incrementing unique ID
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Links to the sessions table
    session_id TEXT,
    
    -- Test subject (e.g., "World War 2 Quiz")
    topic TEXT,
    
    -- Points earned (e.g., 8 out of 10)
    score INTEGER,
    
    -- Total number of questions in the test
    total_questions INTEGER,
    
    -- URL/path to the generated PDF exam (e.g., "/reports/exam_123.pdf")
    pdf_url TEXT,
    
    -- When the test was taken
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

**Example Data**:
| id | session_id | topic | score | total_questions | pdf_url | timestamp |
|----|------------|-------|-------|-----------------|---------|-----------|
| 1 | `abc-123` | "Biology Quiz" | 8 | 10 | `/reports/exam_456.pdf` | `2025-01-15 12:00:00` |

**Use Case**: After taking a quiz, the score and PDF link are saved. Students can review past tests and track improvement over time.

---

##  Table Relationships

```
sessions (1) ──────┬─────── (many) interactions
                   │
                   ├─────── (many) study_sessions
                   │
                   └─────── (many) exam_results
```

**Key Points**:
- One session can have **many** interactions, study sessions, and exam results
- Foreign keys ensure **data integrity** (can't log data for non-existent sessions)
- `session_id` is the **primary link** between all tables

---

##  Setup Script (Python)

**File**: `database_tool.py` (already implemented)

This script initializes the database and creates all tables:

```python
import sqlite3
import os

# Database file location (in the backend root directory)
DB_FILE = "shisui_history.db"

def init_db():
    """
    Initializes the SQLite database with all required tables.
    Safe to run multiple times (uses CREATE TABLE IF NOT EXISTS).
    """
    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ========================================
    # TABLE 1: sessions
    # ========================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,              -- Unique student identifier
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- First login time
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Most recent activity
    )
    ''')
    
    # ========================================
    # TABLE 2: interactions
    # ========================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Auto-generated ID
        session_id TEXT,                          -- Which student
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When asked
        user_query TEXT,                          -- Student's question
        agent_response TEXT,                      -- AI's answer
        agent_name TEXT,                          -- Which agent responded
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)  -- Link to sessions
    )
    ''')
    
    # ========================================
    # TABLE 3: study_sessions
    # ========================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Auto-generated ID
        session_id TEXT,                          -- Which student
        topic TEXT,                               -- Study subject
        duration_minutes INTEGER,                 -- Timer length
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When started
        completed BOOLEAN DEFAULT FALSE,          -- Finished or canceled?
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)  -- Link to sessions
    )
    ''')
    
    # ========================================
    # TABLE 4: exam_results
    # ========================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Auto-generated ID
        session_id TEXT,                          -- Which student
        topic TEXT,                               -- Test subject
        score INTEGER,                            -- Points earned
        total_questions INTEGER,                  -- Total questions
        pdf_url TEXT,                             -- Link to PDF exam
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When taken
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)  -- Link to sessions
    )
    ''')
    
    # Save changes and close connection
    conn.commit()
    conn.close()
    print(f" Database initialized successfully at {DB_FILE}")

# Run this script directly to create the database
if __name__ == "__main__":
    init_db()
```

---

##  How to Use This Script

### **Option 1: Run Directly which is usually the fastest unless unajichukia**
```bash
cd Shisui-backend/tools
python database_tool.py
```
This will create `shisui_history.db` in the backend root.

### **Option 2: Auto-Initialize**
The database is **automatically initialized** when any function in `database_tool.py` is called (e.g., `log_interaction()`). No manual setup needed!

---

##  Common Database Operations

### **1. Log a Chat Interaction**
```python
from tools.database_tool import log_interaction

log_interaction(
    session_id="abc-123",
    user_query="Explain photosynthesis",
    agent_response="Photosynthesis is the process...",
    agent_name="course"
)
```

### **2. Retrieve Student History**
```python
from tools.database_tool import get_student_history

history = get_student_history(session_id="abc-123", limit=10)
# Returns JSON: {"history": [{timestamp, query, response, agent}, ...]}
```

### **3. Log Exam Result**
```python
from tools.database_tool import log_exam_result

log_exam_result(
    session_id="abc-123",
    topic="Biology Quiz",
    score=8,
    total_questions=10,
    pdf_url="/reports/exam_456.pdf"
)
```

---

##  Viewing the Database

### **Using SQLite Browser** (not sure if this still works but maybe sko certain)
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `shisui_history.db`
3. Browse tables, run queries, inspect data

### **Using Python**
```python
import sqlite3
conn = sqlite3.connect("shisui_history.db")
cursor = conn.cursor()

# View all sessions
cursor.execute("SELECT * FROM sessions")
print(cursor.fetchall())

conn.close()
```

---

##  Implementation Checklist and i just realised its easuer to just make the damn thing than explan how to make it

- [x] Database file: `shisui_history.db`
- [x] Table: `sessions` (tracks student sessions)
- [x] Table: `interactions` (logs Q&A history)
- [x] Table: `study_sessions` (records study timers)
- [x] Table: `exam_results` (stores test scores)
- [x] Foreign key constraints (ensures data integrity)
- [x] Auto-initialization (runs on first use)
- [x] Helper functions (`log_interaction`, `get_student_history`, `log_exam_result`)

---

##  so basically tl dr whatever

1. **SQLite** = Simple, embedded, no-server database
2. **4 Tables** = sessions, interactions, study_sessions, exam_results
3. **Foreign Keys** = All tables link to `sessions` via `session_id`
4. **Auto-Init** = Database creates itself on first use
5. **Already Implemented** = See `database_tool.py` for working code

**now lemme sleep nmechoka ka watu watatu!** 
