# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0033_auto_20150720_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='token',
            field=models.CharField(max_length=100, null=True, default=None),
        ),
    ]
