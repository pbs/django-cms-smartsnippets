# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0002_change_smartsnippetvariable_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smartsnippetvariable',
            options={'ordering': ['position'], 'verbose_name': 'Standard variable'},
        ),
        migrations.AddField(
            model_name='smartsnippetvariable',
            name='position',
            field=models.IntegerField(help_text='The order in which to display the variable in the admin.', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
    ]
