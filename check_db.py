import sqlite3

conn = sqlite3.connect('chronos_ledger.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in SQLite:", cursor.fetchall())

conn.close()