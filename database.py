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

def create_views_indices_triggers():
    conn = create_connection()
    c = conn.cursor()

    # Create Views
    c.execute('''
        CREATE VIEW IF NOT EXISTS user_transactions AS
        SELECT 
            u.id AS user_id,
            u.username,
            u.email,
            t.id AS transaction_id,
            t.date,
            t.amount,
            t.category,
            t.subcategory,
            t.description
        FROM 
            users u
        JOIN 
            transactions t
        ON 
            u.id = t.user_id;
    ''')

    # Create Indices
    c.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);')
    c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions (user_id);')

    # Create Trigger to Prevent Negative Transaction Amounts
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_negative_transaction
        BEFORE INSERT ON transactions
        BEGIN
            SELECT CASE
                WHEN NEW.amount < 0 THEN
                    RAISE(ABORT, 'Transaction amount cannot be negative.')
            END;
        END;
    ''')

    # Create Log Table and Trigger for User Registrations
    c.execute('''
        CREATE TABLE IF NOT EXISTS registration_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS log_user_registration
        AFTER INSERT ON users
        BEGIN
            INSERT INTO registration_log (user_id) VALUES (NEW.id);
        END;
    ''')

    conn.commit()
    conn.close()

