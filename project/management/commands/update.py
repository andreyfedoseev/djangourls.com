from django.conf import settings
from django.core.management.base import NoArgsCommand
from djangodblog.handlers import DBLogHandler
from feeds.utils import harvest_feeds
from packages.utils import harvest_pypi_packages
from trends.delicious import fetch_delicious
from trends.diigo import fetch_diigo
from trends.twitter import fetch_twitter
import logging
import traceback


logging.getLogger().addHandler(DBLogHandler())


class Command(NoArgsCommand):

    help = "Re-harvest and update data."
    
    def handle_noargs(self, **options):
        
        harvested_items_count = 0
        delicious_mentions_count = 0
        twitter_mentions_count = 0
        
        try:
            print "Harvesting feeds..."
            harvested_items_count = harvest_feeds()
            print "%i feed items harvested." % harvested_items_count
        except:
            if settings.DEBUG:
                raise
            else:
                message = "Error when harvesting feeds:\n" + traceback.format_exc()
                logging.error(message)
            
        
        try:
            print "Fetching delicious..."
            delicious_mentions_count = fetch_delicious()
            print "%i delicious items fetched." % delicious_mentions_count
        except:
            if settings.DEBUG:
                raise
            else:
                message = "Error when fetching delicious:\n" + traceback.format_exc()
                logging.error(message)
            

        try:
            print "Fetching twitter..."
            twitter_mentions_count = fetch_twitter()
            print "%i tweets fetched." % twitter_mentions_count
        except:
            if settings.DEBUG:
                raise
            else:
                message = "Error when fetching twitter:\n" + traceback.format_exc()
                logging.error(message)

        try:
            print "Fetching diigo..."
            diigo_mentions_count = fetch_diigo()
            print "%i diigo items fetched." % diigo_mentions_count
        except:
            if settings.DEBUG:
                raise
            else:
                message = "Error when fetching diigo:\n" + traceback.format_exc()
                logging.error(message)

        try:
            print "Harvesting PyPi packages..."
            harvested_pypi_packages_count = harvest_pypi_packages()
            print "%i PyPi packages harvested." % harvested_pypi_packages_count
        except:
            if settings.DEBUG:
                raise
            else:
                message = "Error when harvesting PyPi packages:\n" + traceback.format_exc()
                logging.error(message)

        message = """URLs data updated:
%i items harvested from feeds
%i delicious mentions fetched
%i tweets fetched
%i diigo mentions fetched
%i PyPi packages fetched""" % (harvested_items_count,
                               delicious_mentions_count,
                               twitter_mentions_count,
                               diigo_mentions_count,
                               harvested_pypi_packages_count)
        logging.info(message)
        
        print 'Done!'
        
    
    