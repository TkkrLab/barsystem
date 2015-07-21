# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0036_auto_20150721_1314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Product category', 'verbose_name_plural': 'Product categories'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='bar_code',
            new_name='barcode',
        ),
    ]
