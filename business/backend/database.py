import os
import sqlite3
from backend.config import Config

try:
    import pymysql
    import pymysql.cursors
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

def get_db_connection():
    """
    Returns a database connection. Tries MySQL if USE_MYSQL is enabled,
    otherwise falls back to SQLite for robust local execution.
    """
    if Config.USE_MYSQL and HAS_PYMYSQL:
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return conn, 'mysql'
        except Exception as e:
            print(f"[DB Warning] Could not connect to MySQL ({e}). Falling back to SQLite.")

    # Fallback to SQLite
    os.makedirs(os.path.dirname(Config.SQLITE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'

def init_sqlite_db():
    """Initializes SQLite schema if MySQL is not being used."""
    conn, db_type = get_db_connection()
    if db_type == 'sqlite':
        cursor = conn.cursor()
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS entrepreneurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            village_town TEXT,
            district TEXT,
            state TEXT,
            business_type TEXT,
            business_status TEXT DEFAULT 'Planning',
            years_in_business REAL DEFAULT 0,
            number_of_workers INTEGER DEFAULT 1,
            initial_investment REAL DEFAULT 0,
            monthly_revenue REAL DEFAULT 0,
            monthly_expenses REAL DEFAULT 0,
            current_savings REAL DEFAULT 0,
            existing_loan REAL DEFAULT 0,
            goals TEXT,
            is_onboarded INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS business_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_name TEXT,
            business_category TEXT,
            target_customers TEXT,
            products_services TEXT,
            expected_monthly_sales REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            total_revenue REAL DEFAULT 0,
            total_expenses REAL DEFAULT 0,
            net_profit REAL DEFAULT 0,
            health_score INTEGER DEFAULT 75,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS revenues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            revenue_date TEXT NOT NULL,
            product_service TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS business_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recommendation_text TEXT NOT NULL,
            category TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        ''')
        conn.commit()
        conn.close()

def query_db(query, args=(), one=False, commit=False):
    """Unified query wrapper supporting parameterized queries for both MySQL and SQLite."""
    conn, db_type = get_db_connection()
    try:
        if db_type == 'mysql':
            cursor = conn.cursor()
            # MySQL uses %s placeholder
            formatted_query = query.replace('?', '%s')
            cursor.execute(formatted_query, args)
            if commit:
                conn.commit()
                last_id = cursor.lastrowid
                conn.close()
                return last_id
            rv = cursor.fetchall()
            conn.close()
            return (rv[0] if rv else None) if one else rv
        else:
            # SQLite uses ? placeholder
            cursor = conn.cursor()
            cursor.execute(query, args)
            if commit:
                conn.commit()
                last_id = cursor.lastrowid
                conn.close()
                return last_id
            rv = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return (rv[0] if rv else None) if one else rv
    except Exception as e:
        if conn:
            conn.close()
        raise e
