from django.core.management.base import BaseCommand, CommandError
from barsystem_base.models import Journal, Person

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for person in Person.objects.all():
			total = 0
			for journal in Journal.objects.filter(person=person):
				if journal.items == 0:
					total -= journal.amount
				else:
					total -= journal.amount * journal.items
			print(person, person.amount, total, person.amount - total)
		return