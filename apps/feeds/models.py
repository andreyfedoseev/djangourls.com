from core.models import URL
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feeds.settings import FEED_CATEGORIES, QUESTION_CATEGORY, SNIPPET_CATEGORY, \
    JOB_CATEGORY, COMMUNITY_CATEGORY
import BeautifulSoup
import datetime
import feedparser


class Feed(models.Model):

    url = models.URLField(max_length=300, unique=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    source_url = models.URLField(max_length=300, null=True, blank=True)
    harvested = models.BooleanField(default=False)
    harvested_on = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=FEED_CATEGORIES)

    def __unicode__(self):
        return self.title or self.url

    class Meta:
        verbose_name = _(u"Feed")
        verbose_name_plural = _(u"Feeds")

    def harvest(self):
        parsed = feedparser.parse(self.url)
        now = datetime.datetime.now()
        cnt = 0
        for entry in parsed.entries:
            url = entry.link
            identifier = getattr(entry, 'id', url)
            if FeedItem.objects.filter(feed=self, identifier=identifier).count():
                continue

            title = entry.title
            description = getattr(entry, "summary", None)
            if not description:
                try:
                    description = entry.content[0].value
                except:
                    pass
            if description:
                soup = BeautifulSoup.BeautifulSoup(description)
                for feedflare in soup.findAll("div", {"class": "feedflare"}):
                    feedflare.extract()
                for image in soup.findAll("img"):
                    image.extract()
                description = unicode(soup)

            published_on = getattr(entry, "published_parsed", getattr(entry, "created_parsed", getattr(entry, "updated_parsed", None)))
            if published_on:
                published_on = datetime.datetime(*published_on[:6])
            else:
                published_on = now

            item = FeedItem(feed=self, identifier=identifier, title=title, url=url, published_on=published_on)
            item.description = description
            item.save()
            cnt += 1
        self.harvested_on = now
        self.harvested = True
        self.save()
        return cnt


class FeedItem(URL):

    feed = models.ForeignKey(Feed, db_index=True)
    identifier = models.CharField(max_length=500, db_index=True)
    published_on = models.DateTimeField()

    class Meta:
        ordering = ["-published_on", "-timestamp"]


class QuestionManager(models.Manager):

    def get_query_set(self):
        return super(QuestionManager, self).get_query_set().filter(feed__category=QUESTION_CATEGORY)


class Question(FeedItem):

    objects = QuestionManager()

    class Meta:
        proxy = True
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class SnippetManager(models.Manager):

    def get_query_set(self):
        return super(SnippetManager, self).get_query_set().filter(feed__category=SNIPPET_CATEGORY)


class Snippet(FeedItem):

    objects = SnippetManager()

    class Meta:
        proxy = True
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")


class JobManager(models.Manager):

    def get_query_set(self):
        return super(JobManager, self).get_query_set().filter(feed__category=JOB_CATEGORY)


class Job(FeedItem):

    objects = JobManager()

    class Meta:
        proxy = True
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")


class CommunityManager(models.Manager):

    def get_query_set(self):
        return super(CommunityManager, self).get_query_set().filter(feed__category=COMMUNITY_CATEGORY)


class Community(FeedItem):

    objects = CommunityManager()

    class Meta:
        proxy = True
        verbose_name = _("Community")
        verbose_name_plural = _("Communitys")

