from feeds.models import Feed
import datetime


UPDATE_FREQUENCY = datetime.timedelta(minutes=30)


def harvest_feeds():
    cnt = 0
    now = datetime.datetime.now()
    for feed in Feed.objects.all():
        if feed.harvested_on and (now - feed.harvested_on) < UPDATE_FREQUENCY:
            continue
        cnt += feed.harvest()
    return cnt
            