"""Curses support for avionics system."""
import curses

class Vis:
    def __init__(self, avionics_system):
        self.avionics_system = avionics_system
        
        self.stdscr = curses.initscr()  # Make screen
        curses.noecho()  # Remove text input
        curses.cbreak()  # cbreak mode
        stdscr.keypad(True)  # Allow more input

    def main_process(self):
        self.avionics_system.main_process()

    def menu(self):
        """Main menu."""
        input()
        self.main_process()
        return


    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
