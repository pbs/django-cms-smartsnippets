from django.contrib import admin
from django.db.models import Q
from django.contrib.sites.models import Site
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError


from models import SmartSnippet
from settings import shared_sites, include_orphan, restrict_user


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
            raise ValidationError('No code provided.')
        try:
            Template(code)
        except TemplateSyntaxError, e:
            raise ValidationError(e)
        return code


class SnippetAdmin(admin.ModelAdmin):

    shared_sites = shared_sites
    include_orphan = include_orphan
    restrict_user = restrict_user

    list_filter = ('sites__name', )
    list_display = ('name', 'site_list')
    form = SnippetForm
    change_form_template = 'smartsnippets/change_form.html'

    def site_list(self, template):
        return ", ".join([site.name for site in template.sites.all()])
    site_list.short_description = 'sites'

    def get_readonly_fields(self, request, obj=None):
        ro = ['name', 'template_code', 'sites']
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
