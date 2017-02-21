# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0007_auto_20150502_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='moment',
            field=models.DateTimeField(),
        ),
    ]
