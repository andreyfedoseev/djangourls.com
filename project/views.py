from django.shortcuts import render_to_response
from django.template.context import RequestContext
from feeds.models import Question, Snippet, Job, Community
from trends.models import TrendItem
from packages.models import PyPiPackage
from books.utils import get_books
import random


MAX_ITEMS = 14
MAX_BOOKS = 6


def index(request):

    snippets = Snippet.objects.all()
    if snippets.count() > MAX_ITEMS:
        snippets = snippets[:MAX_ITEMS]

    questions = Question.objects.all()
    if questions.count() > MAX_ITEMS:
        questions = questions[:MAX_ITEMS]

    jobs = Job.objects.all()
    if jobs.count() > MAX_ITEMS:
        jobs = jobs[:MAX_ITEMS]

    community = Community.objects.all()
    if community.count() > MAX_ITEMS:
        community = community[:MAX_ITEMS]

    trends = TrendItem.objects.published()
    if trends.count() > MAX_ITEMS:
        trends = trends[:MAX_ITEMS]

    packages = PyPiPackage.objects.all().order_by("-timestamp")
    if packages.count() > MAX_ITEMS:
        packages = packages[:MAX_ITEMS]

    books = get_books()
    if books:
        size = len(books) >= MAX_BOOKS and MAX_BOOKS or len(books)
        books = random.sample(books, size)
        

    data = {}
    data['snippets'] = snippets
    data['questions'] = questions
    data['jobs'] = jobs
    data['community'] = community
    data['trends'] = trends
    data['packages'] = packages
    data['books'] = books
    
    return render_to_response("index.html", data, RequestContext(request))
