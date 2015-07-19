# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0021_auto_20150506_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special_id',
            field=models.CharField(default=None, null=True, max_length=50),
        ),
    ]
