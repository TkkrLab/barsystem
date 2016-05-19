from django.core.management.base import BaseCommand
from barsystem_base.models import Person, Journal

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            try:
                person_id = input('Enter user ID (or enter to exit): ')
            except EOFError:
                return
            if len(person_id) == 0:
                return
            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist:
                print('Invalid id')
                continue

            print(person.nick_name)

            while True:
                entries = Journal.objects.filter(recipient=person).order_by('-moment')[0:10]
                for entry in entries:
                    print('[{}] {}'.format(entry.id, entry.product.name))

                try:
                    transaction_id = input('Enter transaction ID: ')
                except EOFError:
                    break
                if len(transaction_id) == 0:
                    break

                try:
                    entry = Journal.objects.get(recipient=person, id=transaction_id)
                except Journal.DoesNotExist:
                    print('Invalid transaction')

                print('Transaction: {} {} {} {}'.format(entry.moment, entry.items, entry.amount, entry.product.name))

                confirm = input('Delete this transaction? [y/N] ')
                if confirm == 'y':
                    total = entry.items * entry.amount
                    entry.delete()
                    person.amount += total
                    person.save()

                    print('Transaction undone.')
