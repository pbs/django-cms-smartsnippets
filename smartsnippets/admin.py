from django.contrib import admin
from .models import SmartSnippet

class SnippetAdmin(admin.ModelAdmin):
    pass

admin.site.register(SmartSnippet, SnippetAdmin)
