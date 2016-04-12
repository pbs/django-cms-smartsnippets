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
        migrations.AlterField(
            model_name='dropdownvariable',
            name='choices',
            field=models.CharField(help_text='Enter a comma separated list of choices that will be available in the dropdown variable when adding and configuring the custom component on a page.', max_length=512),
        ),
        migrations.AlterField(
            model_name='smartsnippet',
            name='documentation_link',
            field=models.CharField(help_text='Enter URL (i.e. "http://custom_components/docs/plugin_xy.html") to the extended documentation.', max_length=100, verbose_name='Documentation link', blank=True),
        ),
        migrations.AlterField(
            model_name='smartsnippet',
            name='sites',
            field=models.ManyToManyField(help_text='Select on which sites the custom component will be available.', to='sites.Site', verbose_name=b'sites', blank=True),
        ),
        migrations.AlterField(
            model_name='smartsnippet',
            name='template_path',
            field=models.CharField(help_text='Enter a template (i.e. "custom_components/plugin_xy.html") which will be rendered.', max_length=100, verbose_name='Template path', blank=True),
        ),
        migrations.AlterField(
            model_name='smartsnippetvariable',
            name='name',
            field=models.CharField(help_text='Enter the name of the variable defined in the custom component template. Unallowed characters will be removed when the form is saved.', max_length=50),
        ),
        migrations.AlterField(
            model_name='smartsnippetvariable',
            name='widget',
            field=models.CharField(help_text='Select the type of the variable defined in the custom component template.', max_length=50),
        ),
    ]
