from cache_utils.decorators import cached
import re
import urllib
import urlparse
import requests


URL_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
BLACKLIST_URLS = (
    re.compile("^http://instagr\.am/"),
    re.compile("^http://instagram\.com/"),
    re.compile("^http://yfrog.com/"),
    re.compile("^http[s]?://foursquare\.com/"),
    re.compile("^http[s]?://(www|m)\.facebook\.com/"),
    re.compile("^http[s]?://twitter\.com/\w+/status/"),
    re.compile("^http://(m\.)?tmi\.me/"),
    re.compile("^http://imgur\.com/"),
    re.compile("^http://twitter\.yfrog\.com/"),
    re.compile("^http://twitpic\.com/"),
    re.compile("^http://pics\.lockerz\.com/"),
    re.compile("^http://adf\.ly/"),
)


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


untiny = Untiny()


def clean_url(url):
    """
    Remove superfluous parameters from query string. At the moment all
    parameters starting with `utm_` are removed.
    :param url: URL to be cleaned
    :return: cleaned URL
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


def find_urls(text):
    urls = set()

    for url in re.findall(URL_RE, text):
        url = untiny.extract(url)
        url = clean_url(url)
        try:
            url = requests.get(url).url
        except requests.RequestException:
            continue

        blacklisted = False
        for blacklist_re in BLACKLIST_URLS:
            if blacklist_re.match(url):
                blacklisted = True
                break

        if not blacklisted:
            urls.add(url)

    return urls

