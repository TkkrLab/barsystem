# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0030_auto_20150717_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='member',
            field=models.BooleanField(default=False),
        ),
    ]
