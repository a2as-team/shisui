"""
Quick test to verify MySQL database connection
Run this before starting the main app to ensure database is set up correctly
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.database_tool import _get_conn, init_db
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test MySQL connection"""
    print("="*60)
    print("MySQL Database Connection Test")
    print("="*60)
    
    try:
        print("\n[1/3] Testing database connection...")
        conn = _get_conn()
        print("✓ Successfully connected to MySQL")
        
        print("\n[2/3] Checking database schema...")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['sessions', 'interactions', 'study_sessions', 'exam_results']
        
        print("\nTables found:")
        all_exist = True
        for table in required_tables:
            if table in tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} - MISSING!")
                all_exist = False
        
        if not all_exist:
            print("\n⚠ WARNING: Some tables are missing!")
            print("Please import DB/shisui.sql into your MySQL database")
            cursor.close()
            conn.close()
            return False
        
        print("\n[3/3] Testing database operations...")
        
        # Test insert
        cursor.execute(
            "INSERT INTO sessions (session_id) VALUES (%s) ON DUPLICATE KEY UPDATE last_active = CURRENT_TIMESTAMP",
            ("test_connection_check",)
        )
        conn.commit()
        print("  ✓ Insert operation works")
        
        # Test select
        cursor.execute("SELECT session_id FROM sessions WHERE session_id = %s", ("test_connection_check",))
        result = cursor.fetchone()
        if result:
            print("  ✓ Select operation works")
        
        # Cleanup
        cursor.execute("DELETE FROM sessions WHERE session_id = %s", ("test_connection_check",))
        conn.commit()
        print("  ✓ Delete operation works")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED - Database is ready!")
        print("="*60)
        print("\nYou can now run: python main.py")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\n" + "="*60)
        print("Database Connection Failed")
        print("="*60)
        print("\nTroubleshooting:")
        print("1. Make sure MySQL/MariaDB is running (check XAMPP/WAMP)")
        print("2. Verify database 'shisui' exists")
        print("3. Import DB/shisui.sql to create tables")
        print("4. Check .env file has correct DB credentials:")
        print("   DB_HOST=localhost")
        print("   DB_PORT=3306")
        print("   DB_NAME=shisui")
        print("   DB_USER=root")
        print("   DB_PASSWORD=your_password")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
