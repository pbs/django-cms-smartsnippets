# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_smartsnippets_description(apps, schema_editor):
    SmartSnippet = apps.get_model('smartsnippets', 'SmartSnippet')
    SmartSnippet.objects.all().update(description=models.Func(models.F('description'),
                                                   models.Value('Merlin'),
                                                   models.Value('Media Manager'),
                                                   function='replace'))
    SmartSnippet.objects.all().update(description=models.Func(models.F('description'),
                                                   models.Value('COVE'),
                                                   models.Value('Media Manager'),
                                                   function='replace'))


def update_smartsnippets_name(apps, schema_editor):
    SmartSnippet = apps.get_model('smartsnippets', 'SmartSnippet')
    SmartSnippet.objects.all().update(description=models.Func(models.F('name'),
                                                   models.Value('Merlin'),
                                                   models.Value('Media Manager'),
                                                   function='replace'))
    SmartSnippet.objects.all().update(description=models.Func(models.F('name'),
                                                   models.Value('COVE'),
                                                   models.Value('Media Manager'),
                                                   function='replace'))


def revert(apps, schema_ditor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0005_auto_20160404_0851'),
    ]

    operations = [
        migrations.RunPython(update_smartsnippets_description),
        migrations.RunPython(update_smartsnippets_name)
    ]
