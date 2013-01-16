from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand
from feeds.utils import harvest_feeds
from packages.utils import harvest_pypi_packages
from trends.models import TwitterSearch, TrendItem
import logging


logger = logging.getLogger("djangourls.harvest")


class Command(NoArgsCommand):

    help = "Re-harvest and update data."

    option_list = NoArgsCommand.option_list + (
        make_option('--exclude-feeds',
            action='store_true',
            dest='exclude_feeds',
            default=False,
            help="Don't harvest RSS feeds"),
        make_option('--exclude-trends',
            action='store_true',
            dest='exclude_trends',
            default=False,
            help="Don't harvest trends"),
        make_option('--exclude-packages',
            action='store_true',
            dest='exclude_packages',
            default=False,
            help="Don't harvest packages"),
        )

    def handle_noargs(self, **options):

        harvested_items_count = 0
        tweets_count = 0
        trend_items_count = 0
        harvested_pypi_packages_count = 0

        if not options["exclude_feeds"]:
            try:
                logger.info("Harvesting feeds...")
                harvested_items_count = harvest_feeds()
                logger.info("%i feed items harvested.", harvested_items_count)
            except:
                if settings.DEBUG:
                    raise
                else:
                    logger.exception("Error when harvesting feeds")

        if not options["exclude_trends"]:
            try:
                logger.info("Harvesting twitter...")
                tweets_count = TwitterSearch.harvest()
                logger.info("%i tweets harvested.", tweets_count)
            except:
                if settings.DEBUG:
                    raise
                else:
                    logger.exception("Error when harvesting twitter")

            try:
                logger.info("Fetching trend items...")
                trend_items_count = TrendItem.fetch()
                logger.info("%i trend items fetched.", trend_items_count)
            except:
                if settings.DEBUG:
                    raise
                else:
                    logger.exception("Error when fetching trend items")

        if not options["exclude_packages"]:
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
%i tweets harvested
%i trend items fetched
%i PyPi packages fetched""",
            harvested_items_count,
            tweets_count,
            trend_items_count,
            harvested_pypi_packages_count,
        )

