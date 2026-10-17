#Dashboard.py
import curses
import time
def draw_dashboard(stdscr):
    # Clear screen and turn off automatic echoing of keystrokes
    curses.curs_set(0)
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100) # Refresh rate in milliseconds
    while True:
        # Get current terminal dimensions
        max_y, max_x = stdscr.getmaxyx()
        if max_y < 20 or max_x < 80:
            stdscr.clear()
            stdscr.addstr(0, 0, "Terminal too small! Please resize to at least 80x20.")
            stdscr.refresh()
            continue
        stdscr.clear()
        # Draw Header
        title = " === CHRONOSMATCH HFT TERMINAL DASHBOARD === "
        stdscr.addstr(0, (max_x - len(title)) // 2, title, curses.A_BOLD | curses.A_REVERSE)
        # Draw Order Book Section Box (Top Half)
        stdscr.box()
        stdscr.addstr(2, 2, "LIVE ORDER BOOK (BID / ASK SPREAD)", curses.A_BOLD)
        stdscr.addstr(4, 4, "BIDS (Buy Orders)                  asks (Sell Orders)")
        stdscr.addstr(5, 4, "--------------------                  --------------------")
        stdscr.addstr(6, 4, "100 @ $150.25                         10, 50 @ $150.30")
        stdscr.addstr(7, 4, "200 @ $150.20                         500 @ $150.35")
        # Draw Metrics Section (Bottom Half)
        metrics_start_y = max_y // 2
        stdscr.hline(metrics_start_y, 1, curses.ACS_HLINE, max_x - 2)
        stdscr.addstr(metrics_start_y + 1, 2, "SYSTEM METRICS & LATENCY MONITOR", curses.A_BOLD)
        stdscr.addstr(metrics_start_y + 3, 4, f"Status: RUNNING | Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        stdscr.addstr(metrics_start_y + 4, 4, "Throughput: -- orders/sec | Avg Latency: -- us")
        # Instructions
        stdscr.addstr(max_y - 2, 2, "Press 'q' to exit dashboard.", curses.A_DIM)
        stdscr.refresh()
        # Check for exit key
        key = stdscr.getch()
        if key == ord('q'):
            break
if __name__ == "__main__":
    curses.wrapper(draw_dashboard)