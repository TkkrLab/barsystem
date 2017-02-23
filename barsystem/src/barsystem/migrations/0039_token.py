# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0038_auto_20150721_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('value', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('person', models.ForeignKey(to='barsystem.Person', related_name='person')),
            ],
        ),
    ]
