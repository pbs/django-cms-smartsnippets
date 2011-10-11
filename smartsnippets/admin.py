from django.contrib import admin
from django.db.models import Q
from django.contrib.sites.models import Site

from .models import SmartSnippet
from .settings import shared_sites, include_orphan, restrict_user


class SnippetAdmin(admin.ModelAdmin):

    shared_sites = shared_sites
    include_orphan = include_orphan
    restrict_user = restrict_user

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "sites":
            f = Q()
            if not request.user.is_superuser:
                if self.restrict_user:
                    f |= Q(globalpagepermission__user=request.user)
                    f |= Q(globalpagepermission__group__user=request.user)
                if self.shared_sites:
                    f |= Q(name__in=self.shared_sites)
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
