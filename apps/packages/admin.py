from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from packages.models import PyPiPackage


admin.site.register(PyPiPackage, ModelAdmin)