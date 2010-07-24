from django.db import models
import datetime


class URL(models.Model):
    
    title = models.CharField(max_length=400)
    url = models.URLField(max_length=500)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now) 
    
    class Meta:
        abstract = True
        
    def get_absolute_url(self):
        return self.url