from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'address', 'email_verified', 'enable_2fa',)
    search_fields = ('email', 'first_name', 'last_name', 'phone',)
    list_filter = ('email_verified', 'enable_2fa',)
    ordering = ('-created_at',)


# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'status',)
#     search_fields = ('title',)
#     list_filter = ('status',)
#     ordering = ('-created_at',)