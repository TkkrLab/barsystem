from django.db import models
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class Product(models.Model):
    QUANTITY_TYPE_CHOICES = (
        ('None', _('None')),
        ('enter_numeric', _('Numeric input'))
    )

    name = models.CharField(max_length=100)
    member_price = models.DecimalField(max_digits=10, decimal_places=4)
    standard_price = models.DecimalField(max_digits=10, decimal_places=4)
    type = models.CharField(max_length=100, blank=True, default='')
    barcode = models.CharField(max_length=100, blank=True, default='')

    image = models.ImageField(blank=True, default=None)
    active = models.BooleanField(default=True)
    special = models.BooleanField(default=False)
    special_id = models.CharField(max_length=50, null=True, blank=True, default='')
    quantity_type = models.CharField(max_length=100, blank=True, choices=QUANTITY_TYPE_CHOICES, default='None')
    unit = models.CharField(max_length=10, blank=True, default='')

    category = models.ForeignKey('ProductCategory', null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def get_price(self, person, quantity=Decimal(1)):
        return (self.member_price
                if isinstance(person, Person) and person.member and person.amount >= Decimal(0)
                else self.standard_price
                ) * quantity

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Person(models.Model):
    first_name = models.CharField(blank=True, default='', max_length=100)
    last_name = models.CharField(blank=True, default='', max_length=100)
    nick_name = models.CharField(max_length=100)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    type = models.CharField(max_length=100, blank=True, default='')

    active = models.BooleanField(default=True)
    member = models.BooleanField(default=False)
    special = models.BooleanField(default=False)
    allow_remote_access = models.BooleanField(default=False)
    remote_passphrase = models.CharField(blank=True, default='', max_length=50)

    def get_balance(self):
        return self.amount

    def set_balance(self, x):
        self.amount = x

    balance = property(get_balance, set_balance)
    balance_limit = models.DecimalField(null=True, blank=True, default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nick_name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')


class Token(models.Model):
    person = models.ForeignKey('Person', related_name='person')
    value = models.CharField(max_length=64)
    type = models.CharField(max_length=32)


class Journal(models.Model):
    moment = models.DateTimeField()
    sender = models.ForeignKey('Person', related_name='sender', null=True, blank=True, default=None)
    recipient = models.ForeignKey('Person', related_name='recipient', null=True, blank=True, default=None)
    product = models.ForeignKey('Product', null=True, blank=True, default=None)
    items = models.DecimalField(max_digits=10, decimal_places=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # total = models.DecimalField(max_digits=10, decimal_places=4)

    # def __str__(self):
    #     return '{}; {}; {}; {}; {}'.format(
    #         localtime(self.moment),
    #         self.person,
    #         self.product,
    #         self.items,
    #         self.amount)#, self.total)

    @property
    def total(self):
        return self.items * self.amount

    class Meta:
        verbose_name = _('journal entry')
        verbose_name_plural = _('journal entries')


class VendingMachineProduct(models.Model):
    product = models.ForeignKey('Product')
    code = models.CharField(max_length=10)
    virtual = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.product, self.code)
