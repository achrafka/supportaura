# tickets/admin.py
from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['id', 'subject', 'status', 'priority', 'created_by',
                    'assigned_to', 'created_at']
    search_fields = ['subject', 'description']
    list_filter = ['status', 'priority', 'created_at']


admin.site.register(Ticket, TicketAdmin)
