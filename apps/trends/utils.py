from cache_utils.decorators import cached
import re
import urllib
import urlparse
import requests


class Untiny(object):

    SERVICES_URL = "http://untiny.me/api/1.0/services/"
    EXTRACT_URL = "http://untiny.me/api/1.0/extract/"

    @cached(60 * 60 * 24)  # Cache for 1 day
    def get_services(self):
        """
        Get a set of tiny URL services from untiny.me.
        This set consists of domain names.
        """
        try:
            response = requests.get(
                Untiny.SERVICES_URL,
                params=dict(format="text")
            )
        except requests.RequestException:
            return set()

        return set([s.strip() for s in response.text.split(',')])

    def is_tiny(self, url):
        """
        Check if the provided URL is tiny.
        """
        return urlparse.urlsplit(url).netloc in self.get_services()

    @cached(60 * 60 * 24)  # Cache for 1 day
    def extract(self, url):
        """
        Return an untinied version of the given URL.
        If the URL is not tiny it's returned unchanged.
        The method is called recursively to extract URLs 'tinyfied' multiple
        times.
        """
        if not self.is_tiny(url):
            return url
        try:
            response = requests.get(
                Untiny.EXTRACT_URL,
                params=dict(
                    format="text",
                    url=url,
                )
            )
        except requests.RequestException:
            return url

        return self.extract(response.text)


class URLFinder(object):

    URL_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
    BLACKLIST_DOMAINS = set([
        "instagr.am",
        "instagram.com",
        "yfrog.com",
        "foursquare.com",
        "www.facebook.com",
        "m.facebook.com",
        "twitter.com",
        "tmi.me",
        "m.tmi.me",
        "imgur.com",
        "twitter.yfrog.com",
        "twitpic.com",
        "pics.lockerz.com",
        "adf.ly",
    ])

    def __init__(self):
        self.untiny = Untiny()

    def clean_params(self, url):
        """
        Remove superfluous parameters from query string. At the moment all
        parameters starting with `utm_` are removed.
        """
        try:
            str(url)
        except UnicodeEncodeError:
            url = urllib.quote(url.encode('utf-8'))
        parts = list(urlparse.urlsplit(url))
        if not parts[3]:
            return url
        query = urlparse.parse_qsl(parts[3])
        query = [
            (param, value)
            for param, value in query
            if not param.startswith("utm_")
        ]
        if query:
            parts[3] = urllib.urlencode(query)
        else:
            parts[3] = ''
        return urlparse.urlunsplit(parts)

    def is_blacklisted(self, url):
        """
        Check if the provided URL should be blacklisted.
        """
        return urlparse.urlsplit(url).netloc in URLFinder.BLACKLIST_DOMAINS

    def follow_redirects(self, url):
        """
        Follow all redirects from given URL. Return None if the final URL
        can't be accessed.
        """
        try:
            return requests.get(url).url
        except requests.RequestException:
            return None

    def find_urls(self, text):
        urls = set()

        for url in re.findall(self.URL_RE, text):
            url = self.untiny.extract(url)
            url = self.clean_params(url)
            url = self.follow_redirects(url)

            if not self.is_blacklisted(url):
                urls.add(url)

        return urls


url_finder = URLFinder()
