from django.utils.translation import ugettext_lazy as _


QUESTION_CATEGORY = 'question'
SNIPPET_CATEGORY = 'snippet'
JOB_CATEGORY = 'jobs'
COMMUNITY_CATEGORY = 'community'


FEED_CATEGORIES = (
  (QUESTION_CATEGORY, _("Question")),
  (SNIPPET_CATEGORY, _("Snippet")),
  (JOB_CATEGORY, _("Jobs")),
  (COMMUNITY_CATEGORY, _("Community")),
)
