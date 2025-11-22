import application.utils.auth
import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()
ADMIN_PASSWORD_HASH = hash_password("chidok")

# Connect to (or create) a database file
connection = sqlite3.connect("users.db", check_same_thread=False)
cursor = connection.cursor()

# Create a table
# cursor.execute("DROP TABLE IF EXISTS users")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE,
#     account TEXT UNIQUE NOT NULL,
#     password_hash TEXT NOT NULL,
#     failed_attempts INTEGER DEFAULT 0
# )
# """)
# cursor.execute("INSERT INTO users (name, email, account, password_hash) VALUES (?, ?, ?, ?)", ("ChiDok", "dchinh093@gmail.com", "chidok", ADMIN_PASSWORD_HASH))
# cursor.execute("INSERT INTO users (name, email, account, password_hash) VALUES (?, ?, ?, ?)", ("ChiDok", "dchinh094@gmail.com", "a", hash_password("a")))
# connection.commit()

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
    
def db_profile(account):
    cursor.execute("SELECT id, name, email, account FROM users WHERE account = ?", (account,))
    user = cursor.fetchone()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "account": user[3]
        }
    else:
        return None

def db_change_profile(account, name, email):
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE account = ?", (name, email, account))
    connection.commit()
    return True, "Profile updated successfully."

def db_change_password(account, old_password, new_password):
    cursor.execute("SELECT * FROM users WHERE account = ?", (account,))
    user = cursor.fetchone()
    if user and user[4] == hash_password(old_password):
        new_password_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE account = ?", (new_password_hash, account))
        connection.commit()
        return True, "Password changed successfully."
    else:
        return False, "Old password is incorrect."

