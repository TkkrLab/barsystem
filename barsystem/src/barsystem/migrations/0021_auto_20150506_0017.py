# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0020_auto_20150506_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0.0),
        ),
    ]
