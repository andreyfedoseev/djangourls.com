from django.contrib import admin
from trends.models import TwitterSearch, TrendItem
from django.contrib.admin.options import ModelAdmin
from trends.models.trend import BlacklistWord


class TrendItemAdmin(ModelAdmin):

    list_display = ["title", "url", "displayed"]


admin.site.register(TrendItem, TrendItemAdmin)


class TwitterSearchAdmin(ModelAdmin):

    fields = ("term",)


admin.site.register(TwitterSearch, TwitterSearchAdmin)


admin.site.register(BlacklistWord, ModelAdmin)
