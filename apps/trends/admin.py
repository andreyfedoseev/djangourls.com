from django.contrib import admin
from trends.models import TwitterSearch, TrendItem
from django.contrib.admin.options import ModelAdmin
from trends.models.trend import BlacklistWord, WhitelistWord


def link(obj):
    return u"""<a href="{url}" target="_blank">{url}</a>""".format(url=obj.url)
link.allow_tags = True


class TrendItemAdmin(ModelAdmin):

    list_display = ["title", link, "displayed"]
    list_filter = ["displayed"]
    actions = ["make_not_displayed", "re_fetch"]

    def make_not_displayed(self, request, queryset):
        queryset.update(displayed=False)
    make_not_displayed.short_description = "Mark as not displayed"

    def re_fetch(self, request, queryset):
        TrendItem.fetch(queryset)
    re_fetch.short_description = "Re-fetch selected items"


admin.site.register(TrendItem, TrendItemAdmin)


class TwitterSearchAdmin(ModelAdmin):

    fields = ("term",)


admin.site.register(TwitterSearch, TwitterSearchAdmin)


admin.site.register(BlacklistWord, ModelAdmin)
admin.site.register(WhitelistWord, ModelAdmin)
