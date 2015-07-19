# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0017_auto_20150505_2343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='person',
            new_name='sender',
        ),
    ]
