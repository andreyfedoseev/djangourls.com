from django.db import models
from trends.models.trend import Mention, TrendItem
from trends.utils import url_finder
import json
import urllib
import requests


class TwitterSearch(models.Model):

    term = models.CharField(max_length=100)
    last_tweet_id = models.BigIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.term

    class Meta:
        app_label = "trends"
        verbose_name = "Twitter search"
        verbose_name_plural = "Twitter searches"

    @classmethod
    def harvest(cls):

        cnt = 0

        for search in TwitterSearch.objects.all():
            query = {'q': search.term, 'rpp': 100}

            if search.last_tweet_id:
                query['since_id'] = str(search.last_tweet_id)

            try:
                response = requests.get(
                    "http://search.twitter.com/search.json?{0}".format(
                        urllib.urlencode(query)
                    )
                )
            except requests.RequestException:
                return

            response = json.loads(response.text)

            items = response['results']

            for item in items:
                text = item['text']
                tweet_id = item['id']

                for url in url_finder.find_urls(text):
                    # This twitter mention was fetched already, skip this URL
                    if TwitterMention.objects.filter(
                        trend__url=url,
                        tweet_id=tweet_id
                    ).exists():
                        continue

                    trend_item, created = TrendItem.objects.get_or_create(
                        url=url,
                        defaults=dict(
                            title=url
                        )
                    )
                    TwitterMention(trend=trend_item, tweet_id=tweet_id).save()

                cnt += 1

                if items:
                    search.last_tweet_id = items[0]['id']
                    search.save()

        return cnt


class TwitterMention(Mention):

    tweet_id = models.BigIntegerField(db_index=True)

    class Meta:
        app_label = "trends"
