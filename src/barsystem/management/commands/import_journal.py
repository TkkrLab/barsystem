from django.core.management.base import BaseCommand, CommandError
from barsystem_base.models import Journal
import dateutil.parser
import pytz
import os
import re

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import journal'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('Please supply filename')
        if os.path.isfile(args[0]):
            self.import_file(args[0])
        elif os.path.isdir(args[0]):
            journal = os.path.join(args[0], 'journal.csv')
            if os.path.isfile(journal):
                self.import_file(journal)
            else:
                entries = os.listdir(args[0])
                for entry in sorted([os.path.join(args[0], entry) for entry in entries]):
                    if not os.path.isdir(entry):
                        continue
                    journal = os.path.join(entry, 'journal.csv')
                    if os.path.isfile(journal):
                        self.import_file(journal)

            # for dirpath, dirnames, filenames in os.walk(args[0]):
            #     if not re.search(r'\d{4}-\d{2}$', dirpath):
            #         continue
            #     for filename in [os.path.join(dirpath, filename) for filename in filenames if filename == 'journal.csv']:
            #         self.import_file(filename)
        print('Done')

    def import_file(self, filename):
        journal = Journal()
        print('Importing {}'.format(filename))
        with open(filename, 'r') as f:
            columns = None
            for line in f.readlines():
                line = line.strip()
                if not line or len(line) == 0:
                    continue
                line = line.split(',')
                # take header
                if columns is None:
                    columns = line
                    for col in columns:
                        if not hasattr(journal, col):
                            print('Column error: {}'.format(col))
                    continue
                # continue
                values = dict(zip(columns, line))
                if values['person_id'] == '0':
                    values['person_id'] = None
                values['sender_id'] = values['person_id']
                del values['person_id']
                values['moment'] = dateutil.parser.parse(values['moment']).replace(tzinfo=pytz.UTC)

                try:
                    j2 = Journal.objects.get(moment=values['moment'], person=values['person_id'], product=values['product_id'])
                    print('Entry already exists!')
                    continue
                except Journal.DoesNotExist:
                    pass
                #print(values['moment'])
                #continue
                j = Journal()
                for key, val in values.items():
                    if hasattr(j, key):
                        setattr(j, key, val)
                try:
                    print(j)
                except Exception as e:
                    print(values)
                    raise e
                j.save()