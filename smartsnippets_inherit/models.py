from django.db import models
from cms.models import CMSPlugin, Page, Placeholder
from smartsnippets.models import Variable


class InheritPageContent(CMSPlugin):
    # from which page
    from_page = models.ForeignKey(Page)
    # from which section
    from_placeholder = models.CharField(max_length=255, db_index=True)

    def get_placeholder(self):
        try:
            return self.from_page.placeholders.get(slot=self.from_placeholder)
        except Placeholder.DoesNotExist:
            return None


class OverwriteVariable(models.Model):
    # which variable I overwrite
    variable = models.ForeignKey(Variable)
    # overwrite with this value
    value = models.TextField()
    # where I exist
    plugin = models.ForeignKey(
        InheritPageContent, related_name='overwrite_variables')
