from core.models import URL
from django.db import models
from django.utils.html import strip_tags
from guess_language import guessLanguage
import BeautifulSoup
import datetime
import requests


class TrendItemManager(models.Manager):

    MIN_MENTIONS_TO_DISPLAY = 2
    MENTION_LIFETIME = datetime.timedelta(days=7)

    def actual(self):
        qs = super(TrendItemManager, self).get_query_set()
        qs = qs.extra(
            where=["\"trends_mention\".\"timestamp\" > %s"],
            params=[
                datetime.datetime.now() - self.MENTION_LIFETIME
            ]
        )
        qs = qs.annotate(num_mentions=models.Count("mention"))
        qs = qs.filter(num_mentions__gte=self.MIN_MENTIONS_TO_DISPLAY)
        return qs

    def to_fetch(self):
        return self.actual().filter(displayed=None)

    def displayed(self):
        return self.actual().filter(displayed=True).order_by("-timestamp")


class TrendItem(URL):

    displayed = models.NullBooleanField(default=None, db_index=True)
    objects = TrendItemManager()

    class Meta:
        app_label = "trends"

    @classmethod
    def fetch(cls):

        cnt = 0
        for item in TrendItem.objects.to_fetch():
            cnt += 1
            item.displayed = False

            # Try to fetch title from original URL
            try:
                response = requests.get(item.url)
            except requests.RequestException:
                item.save()
                continue

            try:
                soup = BeautifulSoup.BeautifulSoup(response.text)
            except:
                item.save()
                continue

            title = soup.find("title")
            if not title:
                item.save()
                continue

            title = title.renderContents().strip()

            if not title:
                item.save()
                continue

            if not guessLanguage(title).startswith("en"):
                item.save()
                continue

            item.title = title
            meta_description = soup.find("meta", attrs={"name": "description"})
            if meta_description:
                item.description = meta_description["content"]
            else:
                for para in soup.findAll("p"):
                    para_contents = para.renderContents()
                    if len(strip_tags(para_contents)) > 100:
                        item.description = para_contents
                        break

            item.displayed = True
            item.save()

        return cnt


class Mention(models.Model):

    trend = models.ForeignKey(TrendItem)
    timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "trends"
        ordering = ("-timestamp",)




