**# ChronosMatch — Low-Latency HFT Matching Engine & Observability Terminal**
ChronosMatch is a zero-copy High-Frequency Trading (HFT) engine built in Python and Cython to execute order book matching with microsecond-level latency.
This branch (`Avinesh`) contains the ****Member 4**** implementation focusing on the **Terminal User Interface (TUI Dashboard)** and the **SQLite Audit Ledger**.
**## My Role & Responsibilities (Member 4)**
As **Member 4**, I am responsible for building the observability and persistence layer of the ChronosMatch platform:
-> **Terminal UI (`dashboard.py`)**: A live terminal interface built with Python's `curses` library to display order book spreads (Bid/Ask) and system latency metrics in real time.
->**SQLite Ledger (`database.py`)**: A database schema for logging executed trades, order parameters, and system events for post-trade audit and historical tracking.
## 📂 Project Structure (Avinesh Branch)

ChronosMatch/
│
-> dashboard.py -----------------# Terminal dashboard UI using curses
-> database.py ----------- ------# SQLite schema initialization script
-> chronos_ledger.db ----------- # Local SQLite database ledger
-> README.md --------------------# Member 4 documentation
