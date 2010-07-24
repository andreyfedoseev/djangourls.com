from django.conf import settings


AMAZON_ACCESS_KEY = getattr(settings, "AMAZON_ACCESS_KEY", None)
AMAZON_SECRET_KEY = getattr(settings, "AMAZON_SECRET_KEY", None)
AMAZON_LOCALE = getattr(settings, "AMAZON_LOCALE", "us")