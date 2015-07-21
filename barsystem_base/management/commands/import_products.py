from django.core.management.base import BaseCommand, CommandError
from barsystem_base.models import Product

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import list of products'

    csv_columns = 'id,name,sort,items,person_price,cash_price,type,bar_code,stock_value'.split(',')

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('Please supply filename')
        with open(args[0], 'r') as f:
            columns = None
            for line in [line.strip().split(',') for line in f.readlines()]:
                # take header
                if columns is None:
                    columns = line
                    continue
                values = dict(zip(columns, line))

                values['active'] = values['type'] == 'normal'
                values['special'] = values['type'] == 'special'
                values['barcode'] = values['bar_code']
                del values['bar_code']
                p = Product()
                for key, val in values.items():
                    if hasattr(p, key):
                        setattr(p, key, val)
                print(p)
                p.save()
        print('Done')