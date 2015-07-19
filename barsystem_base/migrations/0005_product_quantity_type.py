# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0004_auto_20150430_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(blank=True, max_length=100, default=None),
        ),
    ]
