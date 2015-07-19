# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0028_auto_20150506_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='special',
            field=models.BooleanField(default=False),
        ),
    ]
