import sqlite3

conn = sqlite3.connect('chronos_ledger.db')
cursor = conn.cursor()

print("--- SYSTEM LOGS ---")
cursor.execute("SELECT * FROM system_logs;")
logs = cursor.fetchall()
for log in logs:
    print(log)

print("\n--- EXECUTED TRADES ---")
cursor.execute("SELECT * FROM executed_trades;")
trades = cursor.fetchall()
for trade in trades:
    print(trade)

conn.close()