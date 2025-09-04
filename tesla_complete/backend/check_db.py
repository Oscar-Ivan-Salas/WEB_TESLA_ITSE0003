import os
import sqlite3
from pathlib import Path

def check_database():
    db_path = Path("e:/WEB_TESLA_ITSE0003/tesla_complete/backend/data/tesla.db")
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print("\n📋 Database Status:")
        print(f"📂 Database path: {db_path}")
        print(f"🔢 Size: {db_path.stat().st_size / 1024:.2f} KB")
        print(f"📊 Tables found: {', '.join(tables) if tables else 'None'}")
        
        # Check services count if table exists
        if 'servicios' in tables:
            cursor.execute("SELECT COUNT(*) FROM servicios")
            count = cursor.fetchone()[0]
            print(f"\n🛠️  Services in database: {count}")
            
            # Show first 3 services as sample
            cursor.execute("SELECT id, nombre, categoria FROM servicios LIMIT 3")
            print("\n🔍 Sample services:")
            for row in cursor.fetchall():
                print(f"- {row[0]}: {row[1]} ({row[2]})")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error checking database: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database()
