# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0009_auto_20150503_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='total',
        ),
        migrations.AlterField(
            model_name='journal',
            name='person',
            field=models.ForeignKey(null=True, to='barsystem_base.Person'),
        ),
    ]
