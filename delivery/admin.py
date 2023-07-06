from django.contrib import admin
from . models import *

# Register your models here.

class WilayaAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    class Media:
        js = ("js/wilayas_admin.js",)

class CommuneAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/communes_admin.js",)


admin.site.register(Setting)

admin.site.register(Wilaya,WilayaAdmin)
admin.site.register(Commune,CommuneAdmin)