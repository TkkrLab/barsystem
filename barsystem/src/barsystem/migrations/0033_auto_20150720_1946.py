# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0032_auto_20150720_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='type',
            field=models.CharField(null=True, default=None, blank=True, max_length=100),
        ),
    ]
