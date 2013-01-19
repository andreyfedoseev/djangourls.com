from django.core.cache import cache
import re
import urllib
import urlparse
import requests


_marker = object()


URL_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
CLEANED_QUERY_PARAMS = ('utm_source', 'utm_medium', 'utm_hp_ref')
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


def get_tiny_url_re():
    cache_key = "get_tiny_url_re"
    result = cache.get(cache_key, _marker)
    if result != _marker:
        return result
    try:
        response = requests.get(
            "http://untiny.me/api/1.0/services/?format=text"
        )
    except requests.RequestException:
        response = None

    if response:
        services = [s.strip() for s in response.text.split(',')]
        result = re.compile(
            r'|'.join(r'^http://%s' % service for service in services)
        )
    else:
        result = None
    cache.set(cache_key, result, 60 * 60 * 24)
    return result


def untiny_url(url):
    cache_key = "untiny_url" + url
    result = cache.get(cache_key, _marker)
    if result != _marker:
        return result
    try:
        response = requests.get(
            "http://untiny.me/api/1.0/extract/?format=text&url={0}".format(
                urllib.quote(url)
            )
        )
    except requests.RequestException:
        response = None

    if response:
        response = response.text

        try:
            if re.match(URL_RE, response) and not url.startswith(response):
                result = response
                tiny_urls_re = get_tiny_url_re()
                if tiny_urls_re and re.match(tiny_urls_re, result):
                    result = untiny_url(result)
            else:
                result = None
        except UnicodeDecodeError:
            result = None
    else:
        result = None
    cache.set(cache_key, result, 60 * 60 * 24)
    return result


def clean_url(url):
    try:
        str(url)
    except UnicodeEncodeError:
        url = urllib.quote(url.encode('utf-8'))
    parts = list(urlparse.urlsplit(url))
    if not parts[3]:
        return url
    query = urlparse.parse_qsl(parts[3])
    query = [
        (param, value) for param, value in query
        if param not in CLEANED_QUERY_PARAMS
    ]
    if query:
        parts[3] = urllib.urlencode(query)
    else:
        parts[3] = ''
    return urlparse.urlunsplit(parts)


def find_urls(text):
    urls = set()

    tiny_urls_re = get_tiny_url_re()

    for url in re.findall(URL_RE, text):
        if tiny_urls_re and re.match(tiny_urls_re, url):
            url = untiny_url(url)
        if not url:
            continue

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

