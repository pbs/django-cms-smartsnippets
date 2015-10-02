# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0003_change_smartsnippetvariable_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smartsnippet',
            options={'ordering': ['name'], 'verbose_name': 'Component'},
        ),
    ]
