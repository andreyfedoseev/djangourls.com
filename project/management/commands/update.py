from django.conf import settings
from django.core.management.base import NoArgsCommand
from feeds.utils import harvest_feeds
from packages.utils import harvest_pypi_packages
from trends.twitter import fetch_twitter
import logging


logger = logging.getLogger("djangourls.harvest")


class Command(NoArgsCommand):

    help = "Re-harvest and update data."

    def handle_noargs(self, **options):

        harvested_items_count = 0
        twitter_mentions_count = 0
        harvested_pypi_packages_count = 0

        try:
            logger.info("Harvesting feeds...")
            harvested_items_count = harvest_feeds()
            logger.info("%i feed items harvested.", harvested_items_count)
        except:
            if settings.DEBUG:
                raise
            else:
                logger.exception("Error when harvesting feeds")

        try:
            logger.info("Fetching twitter...")
            twitter_mentions_count = fetch_twitter()
            logger.info("%i tweets fetched.", twitter_mentions_count)
        except:
            if settings.DEBUG:
                raise
            else:
                logger.exception("Error when fetching twitter")

        try:
            logger.info("Harvesting PyPi packages...")
            harvested_pypi_packages_count = harvest_pypi_packages()
            logger.info("%i PyPi packages harvested.", harvested_pypi_packages_count)
        except:
            if settings.DEBUG:
                raise
            else:
                logger.exception("Error when harvesting PyPi packages")

        logger.info(
            """Done! Results:
%i items harvested from feeds
%i tweets fetched
%i PyPi packages fetched""",
            harvested_items_count,
            twitter_mentions_count,
            harvested_pypi_packages_count,
        )

