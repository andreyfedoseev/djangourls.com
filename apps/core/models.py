from django.db import models


class URL(models.Model):

    title = models.CharField(max_length=400)
    url = models.URLField(max_length=500, db_index=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return self.title

