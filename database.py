import sqlite3
def init_ledger_db(db_name="chronos_ledger.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Create Trades Table for executed orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS executed_trades (
            trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            buy_order_id INTEGER,
            sell_order_id INTEGER,
            price REAL,
            quantity INTEGER,
            latency_ns INTEGER,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Create Audit Log Table for system events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_level TEXT,
            message TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"SQLite ledger database '{db_name}' initialized successfully with required tables.")
if __name__ == "__main__":
    init_ledger_db()