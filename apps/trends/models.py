from core.models import URL
from django.db import models
from django.db.models.aggregates import Count
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
import requests
from trends.settings import MIN_MENTIONS_TO_PUBLISH
import BeautifulSoup
import datetime
import json
import urllib


class TrendItemManager(models.Manager):

    def published(self):
        qs = super(TrendItemManager, self).get_query_set()
        qs = qs.filter(broken=False, published=True).order_by("-timestamp")
        qs = qs.annotate(num_mentions=Count("mention"))
        return qs


class TrendItem(URL):

    broken = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    objects = TrendItemManager()

    def _fetch(self):

        # Try to fetch title from original URL
        try:
            response = requests.get(self.url)
        except requests.RequestException:
            self.broken = True
            return
        if not response:
            self.broken = True
            return
        try:
            soup = BeautifulSoup.BeautifulSoup(response.text)
        except:
            self.broken = True
            return
        title = soup.find("title")
        if not title:
            self.broken = True
            return

        title = title.renderContents()

        try:
            detect_lang_response = requests.get(
                "http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q={0}".format(
                    urllib.quote(title)
                )
            )
            detect_lang_result = json.loads(detect_lang_response.text)
            if detect_lang_result["responseData"] and \
               detect_lang_result["responseData"]["isReliable"] and \
               not detect_lang_result["responseData"]["language"].startswith("en"):
                self.broken = True
                return
        except requests.RequestException:
            pass

        self.title = title
        meta_description = soup.find("meta", attrs={"name": "description"})
        if meta_description:
            self.description = meta_description["content"]
        else:
            for para in soup.findAll("p"):
                para_contents = para.renderContents()
                if len(strip_tags(para_contents)) > 100:
                    self.description = para_contents
                    break


class TwitterSearch(models.Model):

    term = models.CharField(max_length=100)
    last_tweet_id = models.BigIntegerField(null=True, blank=True)
    bad_words = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.term

    class Meta:
        verbose_name = _("Twitter search")
        verbose_name_plural = _("Twitter searches")


class Mention(models.Model):

    trend = models.ForeignKey(TrendItem)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-timestamp",)

    def save(self, *args, **kwargs):
        super(Mention, self).save(*args, **kwargs)
        if not self.trend.published and self.trend.mention_set.count() >= MIN_MENTIONS_TO_PUBLISH:
            if self.trend.url and not self.trend.title and not self.trend.broken:
                self.trend._fetch()
            self.trend.published = True
            self.trend.timestamp = datetime.datetime.now()
            self.trend.save()


class TwitterMention(Mention):

    tweet_id = models.BigIntegerField()
