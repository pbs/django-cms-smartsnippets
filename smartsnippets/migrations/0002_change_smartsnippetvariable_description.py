# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartsnippetvariable',
            name='name',
            field=models.CharField(help_text='Enter the name of the variable defined in the smart snippet template. Unallowed charactes will be removed when the form is saved.', max_length=50),
            preserve_default=True,
        ),
    ]
