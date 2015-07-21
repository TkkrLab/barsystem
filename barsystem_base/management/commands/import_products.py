from django.core.management.base import BaseCommand, CommandError
from barsystem_base.models import Product

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import list of products'

    csv_columns = 'id,name,sort,items,person_price,cash_price,type,bar_code,stock_value'.split(',')

    column_mapping = {
        'bar_code': 'barcode',
        'person_price': 'member_price',
        'cash_price': 'standard_price'
    }

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
                for old, new in self.column_mapping.items():
                    values[new] = values[old]
                    del values[old]
                p = Product()
                for key, val in values.items():
                    if hasattr(p, key):
                        setattr(p, key, val)
                print(p)
                p.save()
        print('Done')