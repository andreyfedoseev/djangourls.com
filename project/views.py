from django.shortcuts import render_to_response
from django.template.context import RequestContext
from feeds.models import Question, Snippet, Job, Community
from trends.models import TrendItem
from packages.models import PyPiPackage
from books.utils import get_books


MAX_ITEMS = 14
MAX_BOOKS = 6


def index(request):

    snippets = Snippet.objects.all()[:MAX_ITEMS]

    questions = Question.objects.all()[:MAX_ITEMS]

    jobs = Job.objects.all()[:MAX_ITEMS]

    community = Community.objects.all()[:MAX_ITEMS]

    trends = TrendItem.objects.displayed()[:MAX_ITEMS]

    packages = PyPiPackage.objects.all().order_by("-timestamp")[:MAX_ITEMS]

    books = get_books()

    data = {'snippets': snippets, 'questions': questions, 'jobs': jobs,
            'community': community, 'trends': trends, 'packages': packages,
            'books': books}

    return render_to_response("index.html", data, RequestContext(request))
