# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0027_auto_20150506_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='product',
            field=models.ForeignKey(blank=True, null=True, default=None, to='barsystem_base.Product'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, default=None, to='barsystem_base.Person', related_name='recipient'),
        ),
    ]
