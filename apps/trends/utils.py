from django.core.cache import cache
import re
import urllib
import urllib2
import urlparse


_marker = object()


URL_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)
CLEANED_QUERY_PARAMS = ('utm_source', 'utm_medium')



def get_tiny_url_re():
    cache_key = "get_tiny_url_re"
    result = cache.get(cache_key, _marker)
    if result != _marker:
        return result
    try:
        response = urllib2.urlopen("http://untiny.me/api/1.0/services/?format=text")
    except urllib2.URLError:
        response = None
        
    if response:
        services = [s.strip() for s in response.read().split(',')]
        result = re.compile(r'|'.join(r'^http://%s' % service for service in services))
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
        response = urllib2.urlopen("http://untiny.me/api/1.0/extract/?format=text&url=%s" % urllib2.quote(url))
    except urllib2.URLError:
            response = None
        
    if response:
        response = response.read()
        response = response.decode('utf-8')
        try:
            if re.match(URL_RE, response) and not url.startswith(response):
                result = response
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
    query = [(param, value) for param, value in query if param not in CLEANED_QUERY_PARAMS]
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
        if url:
            urls.add(clean_url(url))

    return urls
    
    