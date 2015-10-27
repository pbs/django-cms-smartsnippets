# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0002_change_smartsnippetvariable_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smartsnippetvariable',
            options={'verbose_name': 'Standard variable'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='smartsnippetvariable',
            order_with_respect_to='snippet',
        ),
    ]
