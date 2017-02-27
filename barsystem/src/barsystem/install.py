import curses
import os
import sys

class BarsystemInstaller:
    def main(self, argv):
        # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        # stdscr.clear()
        # stdscr.addstr(0, 0, 'Hello curses')
        # stdscr.addstr("Fiets", curses.color_pair(1))
        # while True:
        #     stdscr.refresh()
        #     key = stdscr.getkey()
        #     if key == 'q':
        #         break

        self.command = argv[0] if len(argv) else ''
        self.argv = argv[1:] if len(argv) > 1 else []

        cmd_name = 'cmd_' + self.command
        if hasattr(self, cmd_name):
            getattr(self, cmd_name)()
        else:
            print('usage()')

    def cmd_init(self):
        print('init!')

    def cmd_generate_secret_key(self):
        settings_module = os.getenv('DJANGO_SETTINGS_MODULE')
        print('gen sec key!', settings_module)


# Main entrypoint for barsystem-install executable
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barsystem.local_settings')

    BarsystemInstaller().main(argv)

if __name__ == '__main__':
    main()
