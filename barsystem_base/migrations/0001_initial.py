# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('moment', models.DateTimeField()),
                ('items', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10)),
                ('total', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(max_length=100, default='', blank=True)),
                ('last_name', models.CharField(max_length=100, default='', blank=True)),
                ('nick_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10, default=0.0)),
                ('type', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=100, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('sort', models.IntegerField()),
                ('items', models.IntegerField()),
                ('person_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('cash_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('type', models.CharField(max_length=100)),
                ('bar_code', models.CharField(max_length=100)),
                ('stock_value', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='journal',
            name='person',
            field=models.ForeignKey(to='barsystem_base.Person'),
        ),
        migrations.AddField(
            model_name='journal',
            name='product',
            field=models.ForeignKey(to='barsystem_base.Product'),
        ),
    ]
