from django.core.management.base import BaseCommand
from django.core.management import call_command

import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('[Barsystem installer]')
        self.generate_secret_key()
        self.migrate()
        self.createsuperuser()
        self.create_initial_db_entries()

    def generate_secret_key(self):
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

    def migrate(self):
        print('[Running migrations]')
        call_command('migrate')

    def createsuperuser(self):
        print('[Creating superuser]')

        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        try:
            superuser = user_model.objects.filter(is_superuser=True)
            print('- There is already a superuser!')
            return
        except user_model.DoesNotExist:
            call_command('createsuperuser')
            print('- Superuser created.')

    def create_initial_db_entries(self):
        print('[Creating necessary database entries]')
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