# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0011_person_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special',
            field=models.BooleanField(default=False),
        ),
    ]
