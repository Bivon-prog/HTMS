from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Delegation, OnBehalfOfGrant, User


@admin.register(OnBehalfOfGrant)
class OnBehalfOfGrantAdmin(admin.ModelAdmin):
    list_display = ['mission', 'assistant', 'official', 'is_active', 'created_at']


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ['delegator', 'deputy', 'starts_at', 'ends_at', 'cancelled_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'department', 'mission', 'is_active', 'date_joined']
    list_filter = ['role', 'department', 'mission', 'is_active', 'date_joined']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'timezone')}),
        ('Permissions', {'fields': ('role', 'department', 'mission', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'department', 'mission'),
        }),
    )

    readonly_fields = ['date_joined', 'created_at', 'updated_at', 'last_login_ip']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if getattr(request.user, 'role', None) == 'Mission_Admin':
            return qs.filter(mission=request.user.mission)
        return qs
