from django.contrib import admin
from trends.models import TwitterSearch, DeliciousSearch, DiigoSearch
from django.contrib.admin.options import ModelAdmin


admin.site.register(TwitterSearch, ModelAdmin)
admin.site.register(DeliciousSearch, ModelAdmin)
admin.site.register(DiigoSearch, ModelAdmin)