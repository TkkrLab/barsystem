# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0018_auto_20150506_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='recipient',
            field=models.ForeignKey(to='barsystem_base.Person', blank=True, related_name='recipient', null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='sender',
            field=models.ForeignKey(to='barsystem_base.Person', related_name='sender', null=True),
        ),
    ]
