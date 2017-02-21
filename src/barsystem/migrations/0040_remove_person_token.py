# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0039_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='token',
        ),
    ]
