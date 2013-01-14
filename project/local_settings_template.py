from project.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
    }
}

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# Don't share this with anybody.
SECRET_KEY = ''

AMAZON_ACCESS_KEY = ""
AMAZON_SECRET_KEY = ""
