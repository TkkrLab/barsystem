# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0022_product_special_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='special_id',
            field=models.CharField(null=True, default=None, blank=True, max_length=50),
        ),
    ]
