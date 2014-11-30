import os
import dotenv


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
dotenv.read_dotenv()


from dj_static import Cling, MediaCling
from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
application = MediaCling(application)
application = Cling(application)
