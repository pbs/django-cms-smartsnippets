from django.contrib import admin
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms.models import BaseInlineFormSet
from django.template import Template, TemplateSyntaxError, \
                            TemplateDoesNotExist, loader
from django.template.loader import render_to_string
from django.template.defaultfilters import unordered_list
from django.forms.widgets import Select

from admin_extend.extend import registered_form, extend_registered, \
    add_bidirectional_m2m

from models import SmartSnippet, SmartSnippetVariable, DropDownVariable
from settings import (
    shared_sites, include_orphan, restrict_user, handle_permissions_checks,
    custom_widgets_resources)
from widgets_pool import widget_pool


class SnippetForm(ModelForm):
    include_orphan = include_orphan

    class Meta:
        model = SmartSnippet

    def __init__(self, *args, **kwargs):
        if 'sites' in self.base_fields:
            # disallow django to validate if empty since it is done
            #   in the clean sites method
            self.base_fields['sites'].required = False
        super(SnippetForm, self).__init__(*args, **kwargs)

    def clean_sites(self):
        empty_sites = Site.objects.get_empty_query_set()
        self.cleaned_data['sites'] = self.cleaned_data.get(
            'sites', empty_sites) or empty_sites

        def ids_list(queryset):
            return list(queryset.values_list('id', flat=True))

        all_in_form = self.base_fields['sites'].queryset
        assigned_in_form = ids_list(self.cleaned_data['sites'])
        unassigned_in_form = ids_list(
            all_in_form.exclude(id__in=assigned_in_form))

        if self.instance.pk:
            assigned_and_unchanged = ids_list(
                self.instance.sites.exclude(id__in=unassigned_in_form))
            all_assigned = assigned_in_form + assigned_and_unchanged
        else:
            all_assigned = assigned_in_form

        self.cleaned_data['sites'] = Site.objects.filter(id__in=all_assigned)

        if not self.include_orphan and not self.cleaned_data['sites']:
                raise ValidationError('This field is required.')
        return self.cleaned_data['sites']

    def clean_template_code(self):
        code = self.cleaned_data.get('template_code', None)
        if not code:
            return code
        try:
            Template(code)
        except TemplateSyntaxError, e:
            raise ValidationError(e)
        return code

    def clean_template_path(self):
        path = self.cleaned_data.get('template_path', None)
        if not path:
            return path
        try:
            loader.get_template(path)
        except TemplateDoesNotExist, e:
            raise ValidationError(e)
        return path


class SnippetVariablesFormSet(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            available_widgets = [widget.__name__ for widget in widget_pool.get_all_widgets()]
            qs = super(SnippetVariablesFormSet, self).get_queryset().filter(widget__in=available_widgets)
            self._queryset = qs
        return self._queryset



class SnippetVariablesAdmin(admin.StackedInline):
    model = SmartSnippetVariable
    extra = 0
    readonly_fields = ['predefined_widgets']

    def predefined_widgets(self, ssvar):
        return render_to_string(
            'smartsnippets/predefined_widgets.html',
            {'widgets': custom_widgets_resources,
             'snippet_var': ssvar})

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'widget':
            kwargs['widget'] = Select(choices=tuple([(x.__name__, x.name) for x in widget_pool.get_all_widgets()]))
        return super(SnippetVariablesAdmin,self).formfield_for_dbfield(db_field, **kwargs)

    @staticmethod
    def _fieldsets(required):
        return (
            (None, {
                'fields': (required, )
            }),
            ('Advanced', {
                'fields': (('resources', 'predefined_widgets'), ),
                'classes': ('collapse', )
            }),
        )


class RegularSnippetVariablesAdmin(SnippetVariablesAdmin):
    formset = SnippetVariablesFormSet
    fieldsets = SnippetVariablesAdmin._fieldsets(('name', 'widget'))


class DropDownVariableAdmin(SnippetVariablesAdmin):
    model = DropDownVariable
    exclude = ('widget',)
    fieldsets = SnippetVariablesAdmin._fieldsets(('name', 'choices'))


class SnippetAdmin(admin.ModelAdmin):
    inlines = [RegularSnippetVariablesAdmin, DropDownVariableAdmin]
    shared_sites = shared_sites
    include_orphan = include_orphan
    restrict_user = restrict_user

    list_filter = ('sites__name', )
    list_display = ('name', 'site_list')
    search_fields = ['name']
    form = SnippetForm
    change_form_template = 'smartsnippets/change_form.html'
    filter_horizontal = ('sites', )

    class Media:
        js = ("admin/js/SmartSnippets.Variables.js",
              "admin/js/SmartSnippets.PredefinedWidgets.js",)

    def site_list(self, template):
        return ", ".join([site.name for site in template.sites.all()])
    site_list.short_description = 'sites'

    def get_readonly_fields(self, request, obj=None):
        if not handle_permissions_checks:
            return super(SnippetAdmin, self)\
                .get_readonly_fields(request, obj=obj)
        ro = self.form.base_fields.keys()
        if request.user.is_superuser or obj is None:
            return []
        if self.restrict_user and self.shared_sites:
            if obj.sites.filter(name__in=self.shared_sites):
                return ro
        return []

    def has_delete_permission(self, request, obj=None):
        if not handle_permissions_checks:
            return super(SnippetAdmin, self)\
                .has_delete_permission(request, obj=obj)
        if request.user.is_superuser or obj is None:
            return True
        if self.restrict_user and self.shared_sites:
            return not bool(obj.sites.filter(name__in=self.shared_sites))
        return True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not handle_permissions_checks:
            return super(SnippetAdmin, self)\
                .formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "sites":
            f = Q()
            if not request.user.is_superuser:
                if self.restrict_user:
                    f |= Q(globalpagepermission__user=request.user)
                    f |= Q(globalpagepermission__group__user=request.user)
            kwargs["queryset"] = Site.objects.filter(f).distinct()
        return (super(SnippetAdmin, self)
                    .formfield_for_manytomany(db_field, request, **kwargs))

    def queryset(self, request):
        q = super(SnippetAdmin, self).queryset(request)
        if not handle_permissions_checks:
            return q
        f = Q()
        if not request.user.is_superuser:
            if self.restrict_user:
                f |= Q(sites__globalpagepermission__user=request.user)
                f |= Q(sites__globalpagepermission__group__user=request.user)
            if self.shared_sites:
                f |= Q(sites__name__in=self.shared_sites)
            if self.include_orphan:
                f |= Q(sites__isnull=True)

        return q.filter(f).distinct()


admin.site.register(SmartSnippet, SnippetAdmin)


@extend_registered
class ExtendedSiteAdminForm(add_bidirectional_m2m(registered_form(Site))):

    snippets = ModelMultipleChoiceField(
        queryset=SmartSnippet.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Snippets',
            is_stacked=False
        )
    )

    def _get_bidirectional_m2m_fields(self):
        return super(ExtendedSiteAdminForm, self).\
            _get_bidirectional_m2m_fields() + [('snippets', 'smartsnippet_set')]

    def clean_snippets(self):
        assigned_snippets = self.cleaned_data['snippets']
        if self.instance.pk is None or include_orphan:
            return assigned_snippets
        pks = [s.pk for s in assigned_snippets]
        # snippets that were previously assigned to this site, but got unassigned
        unassigned_snippets = self.instance.smartsnippet_set.exclude(pk__in=pks)
        snippets_with_no_sites = []
        for snippet in unassigned_snippets:
            if snippet.sites.count() == 1:
                snippets_with_no_sites.append(snippet)
        if snippets_with_no_sites:
            raise ValidationError(
                "Following snippets will remain with no sites assigned: %s" %
                ", ".join(s.name for s in snippets_with_no_sites))
        return assigned_snippets
