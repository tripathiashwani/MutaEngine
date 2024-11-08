from django.contrib import admin

from .models import Company, Address


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name","status"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["street","city","state","zip_code"]
    search_fields = ["street","city"]
    list_filter = ["state"]
    ordering = ["created_at"]