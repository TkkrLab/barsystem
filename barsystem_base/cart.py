import json
from barsystem_base.models import Product, Journal
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

class Cart(dict):
    def __init__(self, data=None, person=None):
        if data:
            super().__init__(data)
        self.person = person
        for k in self.keys():
            self[k] = CartItem(self[k])
            self[k].person = self.person

    def js(self):
        dump = {}
        for k, v in self.items():
            dump[k] = float(v)
        return json.dumps(dump)

    def add_product(self, product, quantity):
        if product.id in self:
            return False
        self[product.id] = Decimal(quantity)

    def can_checkout(self):
        if len(self) == 0:
            return False
        if self.person and not self.person.member:
            total = Decimal(0.0)
            for product_id, quantity in self.items():
                total += Product.objects.get(id=product_id).get_price(self.person, quantity)
            return self.person.balance - total >= self.person.balance_limit

        return True
    def checkout(self, test=False):
        if not self.can_checkout():
            return False
        total = Decimal(0)
        sender = None
        recipient = self.person
        try:
            with transaction.atomic():
                for product_id, quantity in self.items():
                    product = Product.objects.get(id=product_id)
                    entry = Journal()
                    entry.moment = timezone.now()
                    entry.sender = sender
                    entry.recipient = recipient
                    entry.product = product
                    entry.items = quantity
                    entry.amount = product.get_price(recipient)
                    total += entry.items * entry.amount
                    if not test:
                        entry.save()

                if recipient:
                    recipient.amount -= total
                    if not test:
                        recipient.save()
            print(recipient.amount)
        except Product.DoesNotExist:
            raise

        return True


class CartItem(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise KeyError

    @property
    def amount(self):
        return self.product.get_price(self.person) * Decimal(self.quantity)

    @property
    def product(self):
        return Product.objects.get(id=self['product_id'])

    def js(self):
        return json.dumps(self)
