#!/usr/bin/python3
import sqlite3

# Connect to (or create) users.db
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# Insert sample data
sample_users = [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com")
]

cursor.executemany("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", sample_users)

conn.commit()
conn.close()

print("✅ users.db is ready with sample data!")

