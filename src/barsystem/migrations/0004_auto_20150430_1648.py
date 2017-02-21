# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0003_product_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bar_code',
            field=models.CharField(default=None, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='items',
            field=models.IntegerField(default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sort',
            field=models.IntegerField(default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_value',
            field=models.DecimalField(default=None, decimal_places=4, max_digits=10, blank=True),
        ),
    ]
