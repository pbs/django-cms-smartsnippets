# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from smartsnippets.models import SmartSnippet
from django.db import router
from smartsnippets.utils import regex_replace


class Migration(SchemaMigration):

    no_dry_run = True

    def replace(self, orm, old, new):
        smart_snippets = orm.models.get("smartsnippets.smartsnippet").objects\
                        .db_manager(router.db_for_write(SmartSnippet)).all()
        for ss in smart_snippets:
            image_fields = [field.name for field in ss.variables.all() if field.widget in ["ImageField", "OptionalImageField" ]]
            ss.template_code = regex_replace(ss.template_code, old, new, image_fields)
            ss.save()

    def forwards(self, orm):
        self.replace(orm, "its_image_resize", "image_resize")

    def backwards(self, orm):
        self.replace(orm, "image_resize", "its_image_resize")

    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "['name']", 'unique_together': "(('snippet', 'name'),)", 'object_name': 'SmartSnippetVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippet']"}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'smartsnippets.variable': {
            'Meta': {'unique_together': "(('snippet_variable', 'snippet'),)", 'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'snippet_variable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetVariable']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['smartsnippets']