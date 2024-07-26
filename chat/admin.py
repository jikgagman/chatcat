# chat/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('nickname', 'is_staff', 'is_superuser')
    search_fields = ('nickname',)
    ordering = ('nickname',)
    fieldsets = (
        (None, {'fields': ('nickname', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)

