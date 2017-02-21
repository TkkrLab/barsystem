# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0006_product_unit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'verbose_name_plural': 'journal entries', 'verbose_name': 'journal entry'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'people', 'verbose_name': 'person'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'products', 'verbose_name': 'product'},
        ),
        migrations.AlterField(
            model_name='journal',
            name='items',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='journal',
            name='moment',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
