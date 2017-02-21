# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0015_auto_20150505_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='allow_remote_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='balance_limit',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='person',
            name='remote_passphrase',
            field=models.CharField(max_length=50, default='', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(max_length=100, default='None', choices=[('None', 'None'), ('enter_numeric', 'Numeric input')], blank=True),
        ),
    ]
