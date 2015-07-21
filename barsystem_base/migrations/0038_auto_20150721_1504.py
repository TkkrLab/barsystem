# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barsystem_base', '0037_auto_20150721_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='person_price',
            new_name='member_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='cash_price',
            new_name='standard_price',
        ),
    ]
