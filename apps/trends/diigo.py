from BeautifulSoup import BeautifulSoup
from trends.models import TrendItem, DiigoSearch, DiigoMention
from trends.settings import DIIGO_MENTION_LIFETIME
from trends.utils import get_tiny_url_re, untiny_url, clean_url
import datetime
import feedparser
import re
import urllib


def fetch_diigo():

    cnt = 0
    tiny_url_re = get_tiny_url_re()

    for search in DiigoSearch.objects.all():
        
        try:
            feed = feedparser.parse("http://www.diigo.com/rss/tag/%s?tab=153" % urllib.quote(search.tag))
        except:
            continue
    
        latest_timestamp = None
        
        for entry in feed.entries:
            timestamp = getattr(entry, "published_parsed", getattr(entry, "created_parsed", getattr(entry, "updated_parsed", None)))
            if timestamp:
                timestamp = datetime.datetime(*timestamp[:6])
            else:
                continue
            
            if not latest_timestamp:
                latest_timestamp = timestamp
            
            if search.last_fetched and timestamp <= search.last_fetched:
                break
            
            url = clean_url(entry.link)
            if re.match(tiny_url_re, url):
                url = untiny_url(url)
            if not url:
                continue
            
            soup = BeautifulSoup(entry.summary)
            username = soup.find("a", attrs={"href": re.compile("^http://www.diigo.com/user/")}).renderContents()
            
            try:
                # This mention was fetched already, skip this item
                DiigoMention.objects.get(trend__url=url, username=username)
                continue
            except DiigoMention.DoesNotExist:
                pass
            
            try:
                trend_item = TrendItem.objects.get(url=url)
            except TrendItem.DoesNotExist:
                trend_item = TrendItem(url=url)
                trend_item.save()

            if trend_item.broken:
                continue
            
            DiigoMention(trend=trend_item, username=username).save()
            cnt += 1
    
        if latest_timestamp:
            search.last_fetched = latest_timestamp
            search.save()
    
    # Remove old delicious mentions
    old_mentions = DiigoMention.objects.filter(timestamp__lt=(datetime.datetime.now() - DIIGO_MENTION_LIFETIME))
    old_mentions.delete()
    
    return cnt