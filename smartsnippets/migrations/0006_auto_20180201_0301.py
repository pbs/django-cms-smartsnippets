# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re


def update_smartsnippets(apps, schema_editor):
    SmartSnippet = apps.get_model('smartsnippets', 'SmartSnippet')
    smartsnippets = SmartSnippet.objects.all()
    regex = re.compile("(^|[^A-Za-z])(COVE|Merlin)([^A-Za-z]|$)", re.IGNORECASE)
    for ss in smartsnippets:
        ss.name = re.sub(regex, " Media Manager", ss.name)
        ss.description = re.sub(regex, " Media Manager ", ss.description)
        ss.save()


def revert(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('smartsnippets', '0005_auto_20160404_0851'),
    ]

    operations = [
        migrations.RunPython(update_smartsnippets, revert)
    ]
