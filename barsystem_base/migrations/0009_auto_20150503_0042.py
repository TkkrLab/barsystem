# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0008_auto_20150502_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='person',
            field=models.ForeignKey(blank=True, to='barsystem_base.Person'),
        ),
    ]
