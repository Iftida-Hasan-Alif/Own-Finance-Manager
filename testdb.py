import sqlite3

DB_FILE = "finance_manager_advanced.db"

def view_all_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Get all table names
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n--- Contents of Table: {table_name} ---")
            # Query all data from each table
            c.execute(f"SELECT * FROM {table_name}")
            rows = c.fetchall()
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Run the function
view_all_data()
