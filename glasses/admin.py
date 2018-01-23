from django.contrib import admin

from .models import DptGlasses


class DptGlassesAdmin(admin.ModelAdmin):
    list_display = ['kod', 'name', 'pcs', 'price_roz']


admin.site.register(DptGlasses, DptGlassesAdmin)