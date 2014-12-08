from django import forms
from django.forms.models import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from cms.models import Page
from smartsnippets.cms_plugins import variables_media
from smartsnippets.models import Variable
from smartsnippets_inherit.models import InheritPageContent


class InheritPageForm(ModelForm):
    from_page = forms.ModelChoiceField(
        label=_("page"), queryset=Page.objects.drafts())
    site = None

    class Meta:
        model = InheritPageContent
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    @property
    def media(self):
        _media = super(InheritPageForm, self).media
        variables_media(_media, self._cache_variables)
        return _media

    def __init__(self, *args, **kwargs):
        self._cache_variables = []
        super(InheritPageForm, self).__init__(*args, **kwargs)
        site_pages = Page.objects.drafts().on_site(self.site)
        self.fields['from_page'].queryset = site_pages
        if self.instance.pk:
            phd = self.instance.get_placeholder()
            self._cache_variables = Variable.objects.filter(
                snippet__placeholder=phd
            ).select_related('snippet_variable')

    def clean_from_placeholder(self):
        slot = (self.cleaned_data.get('from_placeholder') or '').strip()
        if not slot:
            raise ValidationError('Placeholder name required.')
        return slot

    def clean_from_page(self):
        page = self.cleaned_data.get('from_page')
        if not page:
            raise ValidationError('Page required.')
        if page.site.pk != self.site.pk:
            raise ValidationError(
                'Page does not belong to site %s.' % self.site.domain)
        return page

    def clean(self):
        cleaned_data = super(InheritPageForm, self).clean()
        slot = cleaned_data.get('from_placeholder')
        page = cleaned_data.get('from_page')
        if not page.placeholders.filter(slot=slot).exists():
            valid_slots = ', '.join(list(
                page.placeholders.values_list('slot', flat=True)))
            raise ValidationError(
                'Placeholder with this name does not exist. '
                'Valid choices are: %s' % valid_slots)
        return cleaned_data
