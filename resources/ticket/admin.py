# tickets/admin.py
from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['id', 'subject', 'status', 'priority', 'created_by',
                    'assigned_to', 'created']
    search_fields = ['subject', 'description']
    list_filter = ['status', 'priority', 'created']


admin.site.register(Ticket, TicketAdmin)
