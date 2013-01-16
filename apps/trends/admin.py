from django.contrib import admin
from trends.models import TwitterSearch
from django.contrib.admin.options import ModelAdmin


admin.site.register(TwitterSearch, ModelAdmin)
