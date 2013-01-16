from trends.models import TrendItem, TwitterSearch,\
    TwitterMention
from trends.settings import TWITTER_MENTION_LIFETIME
from trends.utils import find_urls
import json
import datetime
import requests
import urllib


def fetch_twitter():

    cnt = 0

    for search in TwitterSearch.objects.all():

        query = {'q': search.term, 'rpp': 100}

        bad_words = []
        if search.bad_words:
            bad_words = search.bad_words.lower().split()

        if search.last_tweet_id:
            query['since_id'] = str(search.last_tweet_id)

        try:
            response = requests.get(
                "http://search.twitter.com/search.json?{0}".format(
                    urllib.urlencode(query)
                )
            )
        except requests.RequestException:
            continue

        response = json.loads(response.text)

        items = response['results']

        for item in items:
            text = item['text']
            tweet_id = item['id']

            for word in bad_words:
                if word in text.lower():
                    continue

            for url in find_urls(text):
                try:
                    # This twitter mention was fetched already, skip this URL
                    TwitterMention.objects.get(
                        trend__url=url,
                        tweet_id=tweet_id
                    )
                    continue
                except TwitterMention.DoesNotExist:
                    pass

                try:
                    trend_item = TrendItem.objects.get(url=url)
                except TrendItem.DoesNotExist:
                    trend_item = TrendItem(url=url)
                    trend_item.save()
                    if not trend_item.broken and bad_words:
                        text = isinstance(trend_item.title, str) and trend_item.title.decode('utf-8').lower() or trend_item.title.lower()
                        if trend_item.description:
                            text += isinstance(trend_item.description, str) and trend_item.description.decode('utf-8').lower() or trend_item.description.lower()
                        for word in bad_words:
                            if word in text:
                                trend_item.broken = True
                                trend_item.save()
                                break

                if trend_item.broken:
                    continue

                TwitterMention(trend=trend_item, tweet_id=tweet_id).save()

            cnt += 1

        if items:
            search.last_tweet_id = items[0]['id']
            search.save()

    # Remove old twitter mentions
    old_mentions = TwitterMention.objects.filter(
        timestamp__lt=(datetime.datetime.now() - TWITTER_MENTION_LIFETIME)
    )
    old_mentions.delete()

    return cnt
