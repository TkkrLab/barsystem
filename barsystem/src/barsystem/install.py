import os
import sys

from django.core.management import call_command

# Main entrypoint for barsystem-installer executable
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barsystem.local_settings')

    import warnings
    warnings.filterwarnings('ignore')  # ignore the warning about settings

    call_command('install_barsystem', argv)

if __name__ == '__main__':
    main()
