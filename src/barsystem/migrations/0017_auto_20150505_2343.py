# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0016_auto_20150505_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='balance_limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, blank=True),
        ),
    ]
