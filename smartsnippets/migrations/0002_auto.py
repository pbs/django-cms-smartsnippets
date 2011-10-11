# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field sites on 'SmartSnippet'
        db.create_table('smartsnippets_smartsnippet_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('smartsnippet', models.ForeignKey(orm['smartsnippets.smartsnippet'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('smartsnippets_smartsnippet_sites', ['smartsnippet_id', 'site_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field sites on 'SmartSnippet'
        db.delete_table('smartsnippets_smartsnippet_sites')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        'smartsnippets.smartsnippet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SmartSnippet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_code': ('django.db.models.fields.TextField', [], {})
        },
        'smartsnippets.smartsnippetpointer': {
            'Meta': {'object_name': 'SmartSnippetPointer', 'db_table': "'cmsplugin_smartsnippetpointer'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippet']"})
        },
        'smartsnippets.variable': {
            'Meta': {'unique_together': "(('name', 'snippet'),)", 'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['smartsnippets']
