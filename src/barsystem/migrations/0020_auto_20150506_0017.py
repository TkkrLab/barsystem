# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0019_auto_20150506_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
