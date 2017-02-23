# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0025_auto_20150506_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_value',
        ),
    ]
