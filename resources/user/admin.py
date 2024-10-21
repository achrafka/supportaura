
# tickets/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    model = User
    # Fields to display in admin
    list_display = ['email', 'first_name', 'last_name', 'is_staff',
                    'is_active']
    search_fields = ['email']
    ordering = ['email']
    # Fields to edit in admin interface
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',
                                      'phone_number', 'address',
                                      'profile_image', 'entity')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',
                       'is_active')}),)


admin.site.register(User, UserAdmin)
