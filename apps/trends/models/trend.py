from core.models import URL
from django.conf import settings
from django.db import models
from guess_language import guessLanguage
import datetime
import json
import requests


class TrendItemManager(models.Manager):

    MIN_MENTIONS_TO_DISPLAY = 3
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
    def fetch(cls, queryset=None):

        if queryset is None:
            queryset = TrendItem.objects.to_fetch()

        cnt = 0

        blacklist_words = [
            w.lower() for w in BlacklistWord.objects.values_list("word", flat=True)
        ]

        for item in queryset:
            cnt += 1
            item.displayed = False

            response = requests.get(
                "http://www.diffbot.com/api/article",
                params=dict(
                    token=settings.DIFFBOT_TOKEN,
                    url=item.url,
                    summary=""
                )
            )

            response = json.loads(response.text)

            item.title = response.get("title", item.title) or item.title
            item.description = response.get("summary", u"")

            full_text = u" ".join((
                response.get("title", u""),
                response.get("text", u""),
            ))
            full_text_lower = full_text.lower()
            blacklisted = False

            for word in blacklist_words:
                if word in full_text_lower:
                    blacklisted = True

            if blacklisted:
                item.save()
                continue

            if not guessLanguage(full_text).startswith("en"):
                item.save()
                continue

            item.displayed = True
            item.save()

        return cnt


class Mention(models.Model):

    trend = models.ForeignKey(TrendItem)
    timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "trends"
        ordering = ("-timestamp",)


class BlacklistWord(models.Model):

    word = models.CharField(max_length=100)

    def __unicode__(self):
        return self.word

    class Meta:
        app_label = "trends"
