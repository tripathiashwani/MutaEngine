from django.contrib import admin

from .models import SMTP


@admin.register(SMTP)
class SMTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'username', 'is_default',)
    search_fields = ('user__email', 'username',)
    list_filter = ('is_default',)
    ordering = ('-created_at',)