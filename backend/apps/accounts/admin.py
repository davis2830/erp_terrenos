from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AuditLog, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "role", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("phone", "role", "avatar")}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "object_id", "created_at"]
    list_filter = ["action", "model_name"]
    search_fields = ["user__email", "model_name"]
    readonly_fields = ["user", "action", "model_name", "object_id", "details", "ip_address", "created_at"]
