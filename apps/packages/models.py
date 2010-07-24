from django.db import models
from django.utils.translation import ugettext_lazy as _


class PyPiPackage(models.Model):
    
    name = models.CharField(max_length=200, unique=True, db_index=True)
    version = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    
    @property
    def title(self):
        return u"%s %s" % (self.name, self.version)
    
    def get_absolute_url(self):
        return self.url
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ("name", )
        verbose_name = _("PyPi package")
        verbose_name_plural = _("PyPi packages")