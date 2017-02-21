# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0013_auto_20150505_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(blank=True, max_length=100, default=None, null=True),
        ),
    ]
