import mysql.connector
from mysql.connector import Error
import os
import json
from typing import Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL configuration from environment
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'shisui'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
}

def _get_conn():
    """Get MySQL database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

def init_db():
    """
    Initializes the database tables if they don't exist.
    Note: This assumes the database 'shisui' already exists.
    Use the DB/shisui.sql file to create the schema.
    """
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        required_tables = ['sessions', 'interactions', 'study_sessions', 'exam_results']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"Warning: Missing tables: {missing_tables}")
            print("Please run the DB/shisui.sql file to create the database schema.")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Database initialization check failed: {e}")
        raise

def log_interaction(session_id: str, user_query: str, agent_response: str, agent_name: str):
    """Logs a chat interaction."""
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        # Ensure session exists
        cursor.execute(
            "INSERT INTO sessions (session_id) VALUES (%s) ON DUPLICATE KEY UPDATE last_active = CURRENT_TIMESTAMP",
            (session_id,)
        )
        
        # Log interaction
        cursor.execute('''
            INSERT INTO interactions (session_id, user_query, agent_response, agent_name)
            VALUES (%s, %s, %s, %s)
        ''', (session_id, user_query, agent_response, agent_name))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error logging interaction: {e}")
        raise

def get_student_history(session_id: str, limit: int = 10) -> str:
    """
    Retrieves the recent history for a student session.
    
    Args:
        session_id: The session ID to look up
        limit: Number of recent interactions to return
        
    Returns:
        JSON string of the history
    """
    try:
        conn = _get_conn()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT timestamp, user_query, agent_response, agent_name 
            FROM interactions 
            WHERE session_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON serialization
        history = []
        for row in rows:
            row_dict = dict(row)
            if 'timestamp' in row_dict and isinstance(row_dict['timestamp'], datetime):
                row_dict['timestamp'] = row_dict['timestamp'].isoformat()
            history.append(row_dict)
        
        cursor.close()
        conn.close()
        
        return json.dumps({"history": history})
        
    except Error as e:
        print(f"Error getting student history: {e}")
        return json.dumps({"history": [], "error": str(e)})

def log_study_session(session_id: str, topic: str, duration_minutes: int):
    """Logs a study session."""
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        # Ensure session exists
        cursor.execute(
            "INSERT INTO sessions (session_id) VALUES (%s) ON DUPLICATE KEY UPDATE last_active = CURRENT_TIMESTAMP",
            (session_id,)
        )
        
        cursor.execute('''
            INSERT INTO study_sessions (session_id, topic, duration_minutes)
            VALUES (%s, %s, %s)
        ''', (session_id, topic, duration_minutes))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error logging study session: {e}")
        raise

def complete_study_session(study_session_id: int):
    """Marks a study session as completed."""
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE study_sessions 
            SET completed = TRUE 
            WHERE id = %s
        ''', (study_session_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error completing study session: {e}")
        raise

def log_exam_result(session_id: str, topic: str, score: int, total_questions: int, pdf_url: str):
    """Logs an exam result."""
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        # Ensure session exists
        cursor.execute(
            "INSERT INTO sessions (session_id) VALUES (%s) ON DUPLICATE KEY UPDATE last_active = CURRENT_TIMESTAMP",
            (session_id,)
        )
        
        cursor.execute('''
            INSERT INTO exam_results (session_id, topic, score, total_questions, pdf_url)
            VALUES (%s, %s, %s, %s, %s)
        ''', (session_id, topic, score, total_questions, pdf_url))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error logging exam result: {e}")
        raise

def get_exam_results(session_id: str, limit: int = 10) -> str:
    """
    Retrieves recent exam results for a student session.
    
    Args:
        session_id: The session ID to look up
        limit: Number of recent results to return
        
    Returns:
        JSON string of exam results
    """
    try:
        conn = _get_conn()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT id, topic, score, total_questions, pdf_url, timestamp
            FROM exam_results 
            WHERE session_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        
        # Convert datetime objects to strings
        results = []
        for row in rows:
            row_dict = dict(row)
            if 'timestamp' in row_dict and isinstance(row_dict['timestamp'], datetime):
                row_dict['timestamp'] = row_dict['timestamp'].isoformat()
            # Calculate percentage
            if row_dict['total_questions'] > 0:
                row_dict['percentage'] = (row_dict['score'] / row_dict['total_questions']) * 100
            results.append(row_dict)
        
        cursor.close()
        conn.close()
        
        return json.dumps({"exam_results": results})
        
    except Error as e:
        print(f"Error getting exam results: {e}")
        return json.dumps({"exam_results": [], "error": str(e)})

def get_database_tool():
    """Returns the database tool function for agent use"""
    return get_student_history
