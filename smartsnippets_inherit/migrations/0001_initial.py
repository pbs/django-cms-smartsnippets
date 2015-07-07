# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
        ('smartsnippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InheritPageContent',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('from_placeholder', models.CharField(max_length=255, db_index=True)),
                ('from_page', models.ForeignKey(to='cms.Page')),
            ],
            options={
                'db_table': 'cmsplugin_inheritpagecontent',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='OverwriteVariable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('plugin', models.ForeignKey(related_name='overwrite_variables', to='smartsnippets_inherit.InheritPageContent')),
                ('variable', models.ForeignKey(to='smartsnippets.Variable')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
