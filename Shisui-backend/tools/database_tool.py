import sqlite3
import os
import json
from typing import Dict, Any, List
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'shisui_history.db')

def _get_conn():
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initializes the database tables if they don't exist."""
    conn = _get_conn()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
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

def log_interaction(session_id: str, user_query: str, agent_response: str, agent_name: str):
    """Logs a chat interaction."""
    # Ensure db exists
    init_db()
    
    conn = _get_conn()
    cursor = conn.cursor()
    
    # Ensure session exists
    cursor.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))
    cursor.execute("UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?", (session_id,))
    
    cursor.execute('''
        INSERT INTO interactions (session_id, user_query, agent_response, agent_name)
        VALUES (?, ?, ?, ?)
    ''', (session_id, user_query, agent_response, agent_name))
    
    conn.commit()
    conn.close()

def get_student_history(session_id: str, limit: int = 10) -> str:
    """
    Retrieves the recent history for a student session.
    
    Args:
        session_id: The session ID to look up
        limit: Number of recent interactions to return
        
    Returns:
        JSON string of the history
    """
    # Ensure db exists
    init_db()
    
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, user_query, agent_response, agent_name 
        FROM interactions 
        WHERE session_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (session_id, limit))
    
    rows = cursor.fetchall()
    history = [dict(row) for row in rows]
    
    conn.close()
    return json.dumps({"history": history}, default=str)

def log_exam_result(session_id: str, topic: str, score: int, total_questions: int, pdf_url: str):
    """Logs an exam result."""
    init_db()
    conn = _get_conn()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))
    
    cursor.execute('''
        INSERT INTO exam_results (session_id, topic, score, total_questions, pdf_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, topic, score, total_questions, pdf_url))
    
    conn.commit()
    conn.close()

def get_database_tool():
    return get_student_history
