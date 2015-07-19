# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0029_person_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='barsystem_base.Person', null=True, blank=True, default=None),
        ),
    ]
