from django.contrib import admin
from .models import *


class ThumbnailInline(admin.TabularInline):
    model = Thumbnail
    extra = 1  # Number of empty thumbnail forms to display


class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]

admin.site.register(Product, ProductAdmin)

admin.site.register(Collection)
admin.site.register(Tag)