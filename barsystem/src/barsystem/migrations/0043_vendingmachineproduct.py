# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-19 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem', '0042_auto_20160517_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendingMachineProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barsystem.Product')),
            ],
        ),
    ]
