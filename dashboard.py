import curses
import time
import random

def draw_live_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(500) # Refresh every 500ms

    # Mock initial order book data
    bids = [(100, 150.25), (200, 150.20), (150, 150.15)]
    asks = [(50, 150.30), (500, 150.35), (300, 150.40)]

    while True:
        max_y, max_x = stdscr.getmaxyx()

        if max_y < 20 or max_x < 80:
            stdscr.clear()
            stdscr.addstr(0, 0, "Terminal too small! Please resize to at least 80x20.")
            stdscr.refresh()
            continue

        stdscr.clear()

        # Simulate slight live market fluctuations
        if random.random() > 0.5:
            bids[0] = (random.randint(50, 300), round(150.25 + random.uniform(-0.05, 0.05), 2))
            asks[0] = (random.randint(50, 300), round(150.30 + random.uniform(-0.05, 0.05), 2))

        # Draw Header
        title = " === CHRONOSMATCH HFT LIVE ORDER BOOK (WEEK 2) === "
        stdscr.addstr(0, (max_x - len(title)) // 2, title, curses.A_BOLD | curses.A_REVERSE)

        # Draw Order Book Section Box (Top Half)
        stdscr.box()
        stdscr.addstr(2, 2, "LIVE ORDER BOOK (BID / ASK SPREAD)", curses.A_BOLD)
        stdscr.addstr(4, 4, "BIDS (Buy Orders)                  ASKS (Sell Orders)")
        stdscr.addstr(5, 4, "--------------------                  --------------------")
        
        # Render dynamic Bids & Asks
        for i, (qty, price) in enumerate(bids):
            if 6 + i < max_y // 2:
                stdscr.addstr(6 + i, 4, f"{qty} @ ${price:.2f}")

        for i, (qty, price) in enumerate(asks):
            if 6 + i < max_y // 2:
                stdscr.addstr(6 + i, 38, f"{qty} @ ${price:.2f}")

        # Draw Metrics Section (Bottom Half)
        metrics_start_y = max_y // 2
        stdscr.hline(metrics_start_y, 1, curses.ACS_HLINE, max_x - 2)
        stdscr.addstr(metrics_start_y + 1, 2, "SYSTEM METRICS & LATENCY MONITOR", curses.A_BOLD)
        stdscr.addstr(metrics_start_y + 3, 4, f"Status: RUNNING (Live Feed) | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        stdscr.addstr(metrics_start_y + 4, 4, "Throughput: ~100,000 orders/sec | UI Refresh: 500ms")

        # Instructions
        stdscr.addstr(max_y - 2, 2, "Press 'q' to exit dashboard.", curses.A_DIM)

        stdscr.refresh()

        # Check for exit key
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(draw_live_dashboard)