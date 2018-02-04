from django.contrib import admin

from .models import Glasses


class DptGlassesAdmin(admin.ModelAdmin):
    list_display = ['kod', 'name', 'pcs', 'price_roz']


admin.site.register(Glasses, DptGlassesAdmin)