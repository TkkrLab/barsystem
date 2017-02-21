# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0010_auto_20150503_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
