# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

#from smartsnippets.models import Variable
from smartsnippets.models import SmartSnippetVariable
from django.db import router


class Migration(SchemaMigration):

    no_dry_run = True

    def forwards(self, orm):
        self.backwards(orm)
        # Removing unique constraint on 'Variable', fields ['snippet', 'snippet_variable']
        db.delete_unique('smartsnippets_variable', ['snippet_id', 'snippet_variable_id'])

        # Removing unique constraint on 'SmartSnippetVariable', fields ['snippet', 'name']
        db.delete_unique('smartsnippets_smartsnippetvariable', ['snippet_id', 'name'])

        # Adding field 'SmartSnippetVariable.value'
        db.add_column('smartsnippets_smartsnippetvariable', 'value',
                      self.gf('django.db.models.fields.CharField')(max_length=2048, null=True),
                      keep_default=False)

        # Adding field 'SmartSnippetVariable.snippet_plugin'
        db.add_column('smartsnippets_smartsnippetvariable', 'snippet_plugin',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='variables', null=True, to=orm['smartsnippets.SmartSnippetPointer']),
                      keep_default=False)

        # variables = orm.models.get("smartsnippets.variable").objects\
        #                 .db_manager(router.db_for_write(Variable)).all()

        # for v in variables:
        #     print v.snippet_variable.name
        #     SmartSnippetVariable.objects.get_or_create(name=v.snippet_variable.name,
        #                                widget=v.snippet_variable.widget,
        #                                snippet_id=v.snippet_variable.snippet.id,
        #                                value=v.value,
        #                                snippet_plugin_id=v.snippet.id)

    def backwards(self, orm):
        # Deleting field 'SmartSnippetVariable.value'
        db.delete_column('smartsnippets_smartsnippetvariable', 'value')

        # Deleting field 'SmartSnippetVariable.snippet_plugin'
        db.delete_column('smartsnippets_smartsnippetvariable', 'snippet_plugin_id')

        # Adding unique constraint on 'SmartSnippetVariable', fields ['snippet', 'name']
        db.create_unique('smartsnippets_smartsnippetvariable', ['snippet_id', 'name'])

        # Adding unique constraint on 'Variable', fields ['snippet', 'snippet_variable']
        db.create_unique('smartsnippets_variable', ['snippet_id', 'snippet_variable_id'])


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'smartsnippets.dropdownvariable': {
            'Meta': {'ordering': "['name']", 'object_name': 'DropDownVariable', '_ormbases': ['smartsnippets.SmartSnippetVariable']},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'smartsnippetvariable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartsnippets.SmartSnippetVariable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartsnippets.smartsnippet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SmartSnippet'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'documentation_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'template_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'template_path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'smartsnippets.smartsnippetpointer': {
            'Meta': {'object_name': 'SmartSnippetPointer', 'db_table': "'cmsplugin_smartsnippetpointer'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippet']"})
        },
        'smartsnippets.smartsnippetvariable': {
            'Meta': {'ordering': "['name']", 'object_name': 'SmartSnippetVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippet']"}),
            'snippet_plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'null': 'True', 'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'smartsnippets.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'snippet_variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippetVariable']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['smartsnippets']