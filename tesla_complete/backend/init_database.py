import os
import sqlite3
from pathlib import Path

def init_database():
    # Ensure the data directory exists
    db_dir = Path("e:/WEB_TESLA_ITSE0003/tesla_complete/backend/data")
    db_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = db_dir / "tesla.db"
    
    # Read the SQL file
    sql_path = Path("e:/WEB_TESLA_ITSE0003/tesla_complete/backend/init_db.sql")
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Execute the SQL script
        cursor.executescript(sql_script)
        conn.commit()
        print("✅ Database initialized successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name;
        """)
        tables = cursor.fetchall()
        print("\n📊 Tables created:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Verify services were inserted
        cursor.execute("SELECT COUNT(*) FROM servicios")
        count = cursor.fetchone()[0]
        print(f"\n📋 {count} services inserted successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
