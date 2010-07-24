from django.contrib.sites.models import Site


def base_url(request):
    site = Site.objects.get_current()
    return {'BASE_URL':"http://%s" % site.domain}