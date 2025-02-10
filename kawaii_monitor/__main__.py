import curses
from .monitor import main as monitor_main

def run():
    # This wraps the monitor_main function so that stdscr is provided automatically.
    curses.wrapper(monitor_main)

if __name__ == "__main__":
    run()
