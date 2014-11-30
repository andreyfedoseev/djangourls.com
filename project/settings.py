from getenv import env
import dj_database_url
import os


DATABASES = {
    "default": dj_database_url.config(default="sqlite:///project.db"),
}

DEBUG = env("DEBUG", False)
TEMPLATE_DEBUG = DEBUG

# Don't share this with anybody.
SECRET_KEY = ''

TIME_ZONE = env("TIME_ZONE", "America/Chicago")

LANGUAGE_CODE = 'en-us'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Static file configuration
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")
STATIC_URL = "/static/"

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "project.urls"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.markup",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.syndication",
    "django.contrib.staticfiles",
    "django_extensions",
    "gunicorn",
    "south",
    "compressor",
    "robots",
    "feeds",
    "trends",
    "packages",
    "books",
)

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "project.context_processors.base_url",
)

SITE_ID = 1

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
KEY_PREFIX = "djangourls"

DEBUG_TOOLBAR_PATCH_SETTINGS = env("ENABLE_DEBUG_TOOLBAR", False)

DIFFBOT_TOKEN = env("DIFFBOT_TOKEN", "")

AMAZON_ACCESS_KEY = env("AMAZON_ACCESS_KEY", "")
AMAZON_SECRET_KEY = env("AMAZON_SECRET_KEY", "")
