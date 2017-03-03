import curses
import os
import sys

from django.core.management import execute_from_command_line


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

        import django
        django.setup()

        self.command = argv[0] if len(argv) else ''
        self.argv = argv[1:] if len(argv) > 1 else []

        cmd_name = 'cmd_' + self.command
        if hasattr(self, cmd_name):
            getattr(self, cmd_name)()
        else:
            self.cmd_help()

    def _command_list(self):
        return [cmd[len('cmd_'):] for cmd in dir(self) if cmd.startswith('cmd_')]

    def cmd_help(self):
        print('Possible commands:')
        for cmd in self._command_list():
            print(' *', cmd)

    def cmd_init(self):
        self.cmd_generate_secret_key()
        self.cmd_migrate()
        self.cmd_createsuperuser()
        self.cmd_create_initial_db_entries()

    def cmd_update(self):
        print('[Updating barsystem]')
        self.cmd_migrate()

    def cmd_migrate(self):
        print('[Running migrations]')
        execute_from_command_line([
            sys.argv[0],
            'migrate'
        ])

    def cmd_createsuperuser(self):
        print('[Creating superuser]')

        from django.contrib.auth import get_user_model
        for user in get_user_model().objects.all():
            if user.is_superuser:
                print('- There is already a superuser!')
                return

        execute_from_command_line([
            sys.argv[0],
            'createsuperuser'
        ])
        print('- Superuser created.')

    def cmd_generate_secret_key(self):
        print('[Generating secret key]')
        from django.conf import settings
        from django.core.management.utils import get_random_secret_key

        if os.path.exists(settings.SECRET_KEY_FILE):
            print('- Secret file already exists!')
            return

        os.makedirs(settings.CONFIG_DIR, exist_ok=True)

        with open(settings.SECRET_KEY_FILE, 'w') as f:
            f.write(get_random_secret_key())
        print('- Secret key generated.')

    def cmd_create_initial_db_entries(self):
        print('[Creating necesarry database entries]')
        from decimal import Decimal
        from barsystem.models import Product
        try:
            Product.objects.get(special_id='cash_deposit')
            print('- Cash deposit already exists!')
        except Product.DoesNotExist:
            cash_deposit = Product(
                name='Cash deposit',
                member_price=Decimal(-1),
                standard_price=Decimal(-1),
                active=True,
                special=True,
                special_id='cash_deposit',
                quantity_type='enter_numeric',
            )
            cash_deposit.save()
            print('- Cash deposit created.')



# Main entrypoint for barsystem-install executable
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barsystem.local_settings')

    BarsystemInstaller().main(argv)

if __name__ == '__main__':
    main()
