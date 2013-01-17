from django.contrib import admin
from trends.models import TwitterSearch, TrendItem
from django.contrib.admin.options import ModelAdmin
from trends.models.trend import BlacklistWord


class TrendItemAdmin(ModelAdmin):

    list_display = ["title", "url", "displayed"]
    list_filter = ["displayed"]
    actions = ["make_not_displayed"]

    def make_not_displayed(self, request, queryset):
        queryset.update(displayed=False)
    make_not_displayed.short_description = "Mark as not displayed"


admin.site.register(TrendItem, TrendItemAdmin)


class TwitterSearchAdmin(ModelAdmin):

    fields = ("term",)


admin.site.register(TwitterSearch, TwitterSearchAdmin)


admin.site.register(BlacklistWord, ModelAdmin)
