# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0014_auto_20150505_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(default='None', max_length=100, choices=[('None', 'None'), ('', '')], blank=True),
        ),
    ]
