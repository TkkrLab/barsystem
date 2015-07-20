# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0031_person_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='balance_limit',
            field=models.DecimalField(decimal_places=2, blank=True, max_digits=5, default=0, null=True),
        ),
    ]
