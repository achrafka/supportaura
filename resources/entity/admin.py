from django.contrib import admin
from .models import Entity


class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'fake_fqdn', 'rank', 'created', 'modified',
                    'category', 'city', 'country', 'postalcode')
    search_fields = ('name', 'fake_fqdn', 'label', 'city', 'country')
    list_filter = ('category', 'country')
    ordering = ('rank', 'name')
    filter_horizontal = ('permissions',)


admin.site.register(Entity, EntityAdmin)
