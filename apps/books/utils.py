from books.models import BookSearch
from books.settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_LOCALE
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
import amazonproduct
import urllib


def get_books():
    
    if not AMAZON_ACCESS_KEY or not AMAZON_SECRET_KEY:
        return []

    api = amazonproduct.API(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_LOCALE)
    books = {}
    
    for search in BookSearch.objects.all():
        cache_key = 'books.get_books.%s' % md5_constructor(search.__repr__()).hexdigest()
        result = cache.get(cache_key, None)
        if result is None:
            result = {}
            kw = {'ResponseGroup': 'Medium'}
            kw['Keywords'] = search.keywords
            if search.associate_tag:
                kw['AssociateTag'] = search.associate_tag
            if search.browse_node:
                kw['BrowseNode'] = str(search.browse_node)
            for item in api.item_search('Books', **kw).Items.Item:
                data = get_book_data(item)
                result[data['url']] = data
            cache.set(cache_key, result, 3600 * 24)
        books.update(result)
    return list(books.values())


def get_book_data(item):
    data = {}
    if item.ItemAttributes.ProductGroup != 'Book':
        raise Exception("This amazon ID does not refer to book product.")
    data['url'] = urllib.unquote(unicode(item.DetailPageURL))
    data['title'] = unicode(item.ItemAttributes.Title)
    data['description'] = u''
    for r in item.EditorialReviews.EditorialReview:
        if r.Source == 'Product Description':
            data['description'] = unicode(r.Content)
            break
    data['author'] = unicode(getattr(item.ItemAttributes, "Author", u''))
    data['small_image_url'] = unicode(item.SmallImage.URL)  
    data['medium_image_url'] = unicode(item.MediumImage.URL)  
    data['large_image_url'] = unicode(item.LargeImage.URL)
    return data  
