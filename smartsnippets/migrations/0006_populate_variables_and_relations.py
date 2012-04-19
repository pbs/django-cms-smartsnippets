# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.template import Template, VariableNode, loader

class Migration(DataMigration):

    def forwards(self, orm):
        # create variables for all templates using the old auto-detection method
        for snippet in orm.SmartSnippet.objects.all():
            for var_name in self.get_variables_list(snippet):
                snippet.variables.create(name=var_name, widget='TextField')

        # relate snippet instance variable by id instead of name
        for snippet_ptr in orm.SmartSnippetPointer.objects.all():
            for snippet_ptr_var in snippet_ptr.variables.all():
                try:
                    snippet_var = orm.SmartSnippetVariable.objects.get(snippet=snippet_ptr.snippet,
                                                                       name=snippet_ptr_var.name)
                    snippet_ptr_var.snippet_variable = snippet_var
                    snippet_ptr_var.save()
                except orm.SmartSnippetVariable.DoesNotExist:
                    pass # ignore unused snippet variable values and then drop them
        orm.Variable.objects.filter(snippet_variable=None).delete()

    def backwards(self, orm):
        # repopulate variable names from relation
        for variable in orm.Variable.objects.all():
            variable.name = variable.snippet_variable.name
            variable.save()

        # delete variable definitions
        orm.Variable.objects.all().update(snippet_variable=None)
        orm.SmartSnippetVariable.objects.all().delete()

    def get_template(self, snippet):
        if snippet.template_path:
            return None
        else:
            return Template(snippet.template_code)

    def get_variables_list(self, snippet):
        t = self.get_template(snippet)
        result = set()
        if t is None:
            return result

        for node in t.nodelist.get_nodes_by_type(VariableNode):
            v =  getattr(node.filter_expression.var, 'var', None)
            if v and not v.endswith('_'):
                result.add(v)
        return result

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
        'smartsnippets.dropdownvariable': {
            'Meta': {'ordering': "['name']", 'object_name': 'DropDownVariable', '_ormbases': ['smartsnippets.SmartSnippetVariable']},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'smartsnippetvariable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['smartsnippets.SmartSnippetVariable']", 'unique': 'True', 'primary_key': 'True'})
        },
        'smartsnippets.smartsnippet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SmartSnippet'},
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
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'snippet_variable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'null': 'True', 'to': "orm['smartsnippets.SmartSnippetVariable']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['smartsnippets']
