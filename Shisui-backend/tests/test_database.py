"""
Test database functionality and seed fake student history
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.database_tool import (
    init_db,
    log_interaction,
    get_student_history,
    log_exam_result,
    _get_conn
)


# Sample data for seeding
TOPICS = [
    "Python Programming",
    "Data Structures",
    "Machine Learning",
    "Web Development",
    "Database Design",
    "Algorithms",
    "React Fundamentals",
    "API Design",
    "System Design",
    "Computer Networks"
]

SAMPLE_QUERIES = [
    "Can you explain {topic}?",
    "I need help understanding {topic}",
    "What are the key concepts in {topic}?",
    "Give me a quiz on {topic}",
    "I want to study {topic}",
    "Set a timer for studying {topic}",
    "Test my knowledge of {topic}",
    "Find resources about {topic}",
    "What should I know about {topic}?",
    "Help me learn {topic}"
]

SAMPLE_RESPONSES = [
    "Let me help you with {topic}. Here's what you need to know...",
    "Great question! {topic} is an important concept. Let me explain...",
    "I'll search for some resources on {topic} for you.",
    "I've set a 25-minute study timer for {topic}. Let's focus!",
    "Here's a quiz on {topic} to test your understanding.",
    "I've found some excellent materials on {topic}. Let me share them...",
    "Let me break down {topic} into simpler concepts for you.",
    "I'll help you master {topic}. Let's start with the basics...",
    "Perfect! Let's dive into {topic} together.",
    "I've generated a comprehensive study plan for {topic}."
]

AGENT_NAMES = ["planner_agent", "course_agent", "exam_agent"]


def clear_database():
    """Clear all data from the database"""
    print("\n[INFO] Clearing database...")
    
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        cursor.execute("DELETE FROM exam_results")
        cursor.execute("DELETE FROM study_sessions")
        cursor.execute("DELETE FROM interactions")
        cursor.execute("DELETE FROM sessions")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("[SUCCESS] Database cleared")
        
    except Exception as e:
        print(f"[ERROR] Failed to clear database: {e}")
        raise



def seed_student_history(session_id: str, num_interactions: int = 20):
    """
    Seed fake student history for testing
    
    Args:
        session_id: Session ID to seed data for
        num_interactions: Number of interactions to create
    """
    print(f"\n[INFO] Seeding {num_interactions} interactions for session: {session_id}")
    
    # Initialize database
    init_db()
    
    # Create interactions over the past week
    base_time = datetime.now() - timedelta(days=7)
    
    for i in range(num_interactions):
        # Random topic
        topic = random.choice(TOPICS)
        
        # Random query and response
        query_template = random.choice(SAMPLE_QUERIES)
        response_template = random.choice(SAMPLE_RESPONSES)
        
        user_query = query_template.format(topic=topic)
        agent_response = response_template.format(topic=topic)
        agent_name = random.choice(AGENT_NAMES)
        
        # Create timestamp spread over the week
        timestamp_offset = timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        interaction_time = base_time + timestamp_offset
        
        # Log interaction
        log_interaction(session_id, user_query, agent_response, agent_name)
        
        print(f"  [{i+1}/{num_interactions}] Logged: {user_query[:50]}...")
    
    print(f"[SUCCESS] Seeded {num_interactions} interactions")


def seed_exam_results(session_id: str, num_exams: int = 5):
    """
    Seed fake exam results
    
    Args:
        session_id: Session ID to seed data for
        num_exams: Number of exam results to create
    """
    print(f"\n[INFO] Seeding {num_exams} exam results for session: {session_id}")
    
    for i in range(num_exams):
        topic = random.choice(TOPICS)
        total_questions = random.choice([5, 10, 15, 20])
        score = random.randint(int(total_questions * 0.5), total_questions)
        pdf_url = f"/reports/exam_{session_id}_{i+1}.pdf"
        
        log_exam_result(session_id, topic, score, total_questions, pdf_url)
        
        percentage = (score / total_questions) * 100
        print(f"  [{i+1}/{num_exams}] {topic}: {score}/{total_questions} ({percentage:.0f}%)")
    
    print(f"[SUCCESS] Seeded {num_exams} exam results")


def test_database_initialization():
    """Test database initialization"""
    print("\n" + "="*60)
    print("Test 1: Database Initialization")
    print("="*60)
    
    try:
        init_db()
        
        # Check if tables exist
        conn = _get_conn()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['sessions', 'interactions', 'study_sessions', 'exam_results']
        
        print("\n[INFO] Checking for required tables...")
        for table in required_tables:
            if table in tables:
                print(f"  [✓] {table}")
            else:
                print(f"  [✗] {table} - MISSING!")
                conn.close()
                return False
        
        conn.close()
        print("\n[SUCCESS] All tables exist")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Database initialization failed: {str(e)}")
        return False


def test_log_interaction():
    """Test logging interactions"""
    print("\n" + "="*60)
    print("Test 2: Log Interaction")
    print("="*60)
    
    try:
        session_id = "test_session_001"
        user_query = "What is Python?"
        agent_response = "Python is a high-level programming language."
        agent_name = "planner_agent"
        
        print(f"\n[INFO] Logging test interaction...")
        log_interaction(session_id, user_query, agent_response, agent_name)
        
        # Verify it was logged
        history = json.loads(get_student_history(session_id, limit=1))
        
        if len(history['history']) > 0:
            print(f"[SUCCESS] Interaction logged successfully")
            print(f"  Query: {history['history'][0]['user_query']}")
            print(f"  Agent: {history['history'][0]['agent_name']}")
            return True
        else:
            print("[ERROR] No interaction found in database")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Log interaction failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_get_student_history():
    """Test retrieving student history"""
    print("\n" + "="*60)
    print("Test 3: Get Student History")
    print("="*60)
    
    try:
        session_id = "test_session_002"
        
        # Log multiple interactions
        print(f"\n[INFO] Creating test history...")
        for i in range(5):
            log_interaction(
                session_id,
                f"Question {i+1}",
                f"Answer {i+1}",
                random.choice(AGENT_NAMES)
            )
        
        # Retrieve history
        print(f"[INFO] Retrieving history...")
        history_json = get_student_history(session_id, limit=10)
        history = json.loads(history_json)
        
        print(f"\n[SUCCESS] Retrieved {len(history['history'])} interactions")
        print("\nRecent interactions:")
        for idx, interaction in enumerate(history['history'][:3], 1):
            print(f"  {idx}. {interaction['user_query']} -> {interaction['agent_response']}")
        
        return len(history['history']) == 5
        
    except Exception as e:
        print(f"\n[ERROR] Get student history failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_seeded_data():
    """Test with seeded data"""
    print("\n" + "="*60)
    print("Test 4: Seeded Student Data")
    print("="*60)
    
    try:
        session_id = "student_12345"
        
        # Seed data
        seed_student_history(session_id, num_interactions=15)
        seed_exam_results(session_id, num_exams=3)
        
        # Retrieve and display
        print(f"\n[INFO] Retrieving seeded history...")
        history_json = get_student_history(session_id, limit=5)
        history = json.loads(history_json)
        
        print(f"\n[SUCCESS] Retrieved {len(history['history'])} recent interactions")
        print("\nMost recent interactions:")
        for idx, interaction in enumerate(history['history'], 1):
            timestamp = interaction['timestamp']
            query = interaction['user_query'][:60]
            agent = interaction['agent_name']
            print(f"  {idx}. [{timestamp}] ({agent}) {query}...")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Seeded data test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all database tests"""
    print("\n" + "="*70)
    print(" Database & Database Tool Tests")
    print("="*70)
    
    # Clear database first
    clear_database()
    
    results = []
    
    # Run tests
    results.append(("Database Initialization", test_database_initialization()))
    results.append(("Log Interaction", test_log_interaction()))
    results.append(("Get Student History", test_get_student_history()))
    results.append(("Seeded Student Data", test_seeded_data()))
    
    # Summary
    print("\n" + "="*70)
    print(" Test Summary")
    print("="*70)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, r in results if r)
    failed = sum(1 for _, r in results if not r)
    
    print(f"\nResults: {passed} passed, {failed} failed")
    print("="*70)


def seed_multiple_students():
    """Seed data for multiple students"""
    print("\n" + "="*70)
    print(" Seeding Multiple Student Sessions")
    print("="*70)
    
    student_sessions = [
        "student_alice_001",
        "student_bob_002",
        "student_charlie_003",
        "student_diana_004",
        "student_eve_005"
    ]
    
    for session_id in student_sessions:
        print(f"\n--- Seeding {session_id} ---")
        num_interactions = random.randint(10, 25)
        num_exams = random.randint(2, 5)
        
        seed_student_history(session_id, num_interactions)
        seed_exam_results(session_id, num_exams)
    
    print("\n" + "="*70)
    print(f"[SUCCESS] Seeded {len(student_sessions)} student sessions")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--seed-multiple":
        # Seed multiple students
        clear_database()
        seed_multiple_students()
    else:
        # Run tests
        run_all_tests()
