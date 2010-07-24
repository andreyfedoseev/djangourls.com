from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookSearch(models.Model):
    
    keywords = models.CharField(max_length=100)
    browse_node = models.IntegerField(null=True, blank=True)
    associate_tag = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.keywords
    
    class Meta:
        verbose_name = _("Book search")
        verbose_name_plural = _("Book searches")