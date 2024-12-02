import sqlite3

DB_FILE = "finance_manager_advanced.db"

def create_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()

    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Transactions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            amount REAL,
            category TEXT,
            subcategory TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT id FROM users WHERE email = ? AND password = ?
    ''', (email, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]
    return None
