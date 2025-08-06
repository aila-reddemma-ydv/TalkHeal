import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(name, email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Email already registered"
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password(password, result[1]):
        user = {"name": result[0], "email": email}
        return True, user
    return False, None