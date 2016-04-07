# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0004_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smartsnippet',
            options={'ordering': ['name'], 'verbose_name': 'Custom Component', 'verbose_name_plural': 'Custom Components'},
        ),
        migrations.AlterField(
            model_name='smartsnippetpointer',
            name='snippet',
            field=models.ForeignKey(verbose_name=b'Custom Component', to='smartsnippets.SmartSnippet'),
        ),
    ]
