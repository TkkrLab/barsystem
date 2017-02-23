# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0026_remove_product_stock_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='product',
            field=models.ForeignKey(blank=True, to='barsystem.Product', null=True),
        ),
    ]
