from django.contrib import admin
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms.models import BaseInlineFormSet
from django.template import Template, TemplateSyntaxError, \
                            TemplateDoesNotExist, loader
from django.forms.widgets import Select

from admin_extend.extend import registered_form, extend_registered, \
    add_bidirectional_m2m

from models import SmartSnippet, SmartSnippetVariable, DropDownVariable
from settings import shared_sites, include_orphan, restrict_user
from widgets_pool import widget_pool


class SnippetForm(ModelForm):
    include_orphan = include_orphan

    class Meta:
        model = SmartSnippet

    def clean_sites(self):
        if not self.include_orphan:
            if not self.cleaned_data.get('sites', []):
                raise ValidationError('This field is required.')
        return self.cleaned_data.get('sites', [])

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

    def __init__(self, *args, **kwargs):
        super(SnippetVariablesFormSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            available_widgets = [widget.__name__ for widget in widget_pool.get_all_widgets()]
            qs = super(SnippetVariablesFormSet, self).get_queryset().filter(widget__in=available_widgets)
            self._queryset = qs
        return self._queryset


class SnippetVariablesAdmin(admin.StackedInline):
    model = SmartSnippetVariable
    extra = 0
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'widget':
            kwargs['widget'] = Select(choices=tuple([(x.__name__, x.name) for x in widget_pool.get_all_widgets()]))
        return super(SnippetVariablesAdmin,self).formfield_for_dbfield(db_field, **kwargs)



class RegularSnippetVariablesAdmin(SnippetVariablesAdmin):
    formset = SnippetVariablesFormSet


class DropDownVariableAdmin(SnippetVariablesAdmin):
    model = DropDownVariable
    exclude = ('widget',)


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
              "admin/js/cropduster_sizeset.js",)

    def site_list(self, template):
        return ", ".join([site.name for site in template.sites.all()])
    site_list.short_description = 'sites'

    def get_readonly_fields(self, request, obj=None):
        ro = self.form.base_fields.keys()
        if request.user.is_superuser or obj is None:
            return []
        if self.restrict_user and self.shared_sites:
            if obj.sites.filter(name__in=self.shared_sites):
                return ro
        return []

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        if self.restrict_user and self.shared_sites:
            return not bool(obj.sites.filter(name__in=self.shared_sites))
        return True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
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
        if self.instance.pk is None:
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
