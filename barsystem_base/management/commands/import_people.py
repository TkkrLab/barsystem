from django.core.management.base import BaseCommand, CommandError
from barsystem_base.models import Person, Token
from decimal import Decimal

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import list of people'

    csv_columns = 'id,first_name,last_name,nick_name,amount,type,token'.split(',')

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('Please supply filename')
        with open(args[0], 'r') as f:
            columns = None
            for line in [line.strip().split(',') for line in f.readlines() if line[0] != '#']:
                # print(line)
                # take header
                if columns is None:
                    columns = line
                    continue
                values = dict(zip(columns, line))

                try:
                    p = Person.objects.get(id=values['id'])
                except Person.DoesNotExist:
                    p = Person()
                    p.active = values['type'] != 'hidden'
                    p.special = values['type'] == 'special'
                    p.member = True
                    p.balance_limit = Decimal(-13.37)
                for key, val in values.items():
                    if hasattr(p, key):
                        setattr(p, key, val)
                print(p)
                p.save()
                t = Token()
                t.type = 'ibutton'
                t.value = values['token']
                t.person = p
                t.save()
        print('Done')