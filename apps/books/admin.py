from books.models import BookSearch
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin


admin.site.register(BookSearch, ModelAdmin)