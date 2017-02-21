# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0024_auto_20150506_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='items',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sort',
        ),
    ]
