# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0029_person_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='barsystem.Person', null=True, blank=True, default=None),
        ),
    ]
