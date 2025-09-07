import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()
ADMIN_PASSWORD_HASH = hash_password("chidok")

# Connect to (or create) a database file
connection = sqlite3.connect("users.db", check_same_thread=False)
cursor = connection.cursor()

# Create a table
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    account TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0
)
""")
cursor.execute("INSERT INTO users (name, email, account, password_hash) VALUES (?, ?, ?, ?)", ("ChiDok", "dchinh093@gmail.com", "chidok", ADMIN_PASSWORD_HASH))
connection.commit()

def db_login(account, password):
    cursor.execute("SELECT * FROM users WHERE account = ?", (account,))
    user = cursor.fetchone()
    if user:
        if user[5] >= 5:
            return False, "Account locked due to too many failed attempts."
        elif user[4] == hash_password(password):
            cursor.execute("UPDATE users SET failed_attempts = 0 WHERE account = ?", (account,))
            connection.commit()
            return True, "Login successful."
        else:
            cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE account = ?", (account,))
            connection.commit()
            return False, "Invalid credentials."
    else:
        return False, "Invalid credentials."

def db_register(name, email, account, password):
    cursor.execute("SELECT * FROM users WHERE account = ?", (account,))
    user = cursor.fetchone()
    if user:
        return False, "Account already exists."
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (name, email, account, password_hash) VALUES (?, ?, ?, ?)", (name, email, account, password_hash))
    connection.commit()
    return True, "Registration successful."

def db_forgot(username):
    cursor.execute("SELECT * FROM users WHERE account = ? OR email = ?", (username, username))
    user = cursor.fetchone()
    if user:
        return True, f"Function under maintenance"
    else:
        return False, "Username or email not found."
    

