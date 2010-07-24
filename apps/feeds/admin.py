from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from feeds.forms import FeedAdminForm
from feeds.models import Feed


def display_harvested_on(obj):
    if not obj.harvested_on:
        return _(u"Not harvested yet")
    return dateformat.format(obj.harvested_on, settings.DATETIME_FORMAT)
display_harvested_on.short_description = _(u"Harvested on")    


class FeedAdmin(admin.ModelAdmin):

    form = FeedAdminForm
    
    list_display = ('title', 'url', 'harvested', 'category', display_harvested_on)
    list_display_links = ('title', )

    search_fields = ('title', 'url')
    list_filter = ('harvested', 'category')
    
    def harvest(self, request, queryset):
        feeds_count = queryset.count()
        if not feeds_count:
            return
        count = 0
        for feed in queryset:
            count += feed.harvest()
        message = ungettext_lazy(u"%(count)d item was harvested", u"%(count)d items were harvested", count) % {'count': count}
        message += ungettext_lazy(u" from %(count)d feed.", u" from %(count)d feeds.", feeds_count) % {'count': feeds_count}
        self.message_user(request, message)
    harvest.short_description = _(u"Harvest selected feeds")

    actions = ['harvest']
    
    
admin.site.register(Feed, FeedAdmin)
