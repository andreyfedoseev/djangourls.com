from trends.models import TrendItem, DeliciousSearch, DeliciousMention
from trends.settings import DELICIOUS_MENTION_LIFETIME
from trends.utils import get_tiny_url_re, untiny_url, clean_url
import cjson
import datetime
import isodate
import re
import urllib
import urllib2


def fetch_delicious():

    cnt = 0
    tiny_url_re = get_tiny_url_re()

    for search in DeliciousSearch.objects.all():
        
        try:
            response = urllib2.urlopen("http://feeds.delicious.com/v2/json/tag/%s?count=100" % urllib.quote(search.tag))
        except urllib2.URLError:
            continue
    
        items = cjson.decode(response.read())

        for item in items:
            timestamp = isodate.parse_datetime(item['dt']).replace(tzinfo=None)
            if search.last_fetched and timestamp <= search.last_fetched:
                break
            
            url = clean_url(item['u'].replace('\\/', '/'))
            if re.match(tiny_url_re, url):
                url = untiny_url(url)
            if not url:
                continue
            username = item['a']
            
            try:
                # This mention was fetched already, skip this item
                DeliciousMention.objects.get(trend__url=url, username=username)
                continue
            except DeliciousMention.DoesNotExist:
                pass
            
            try:
                trend_item = TrendItem.objects.get(url=url)
            except TrendItem.DoesNotExist:
                trend_item = TrendItem(url=url)
                trend_item.save()

            if trend_item.broken:
                continue
            
            DeliciousMention(trend=trend_item, username=username).save()
            cnt += 1
    
        if items:
            search.last_fetched = isodate.parse_datetime(items[0]['dt']).replace(tzinfo=None)
            search.save()
    
    # Remove old delicious mentions
    old_mentions = DeliciousMention.objects.filter(timestamp__lt=(datetime.datetime.now() - DELICIOUS_MENTION_LIFETIME))
    old_mentions.delete()
    
    return cnt