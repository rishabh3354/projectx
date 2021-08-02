from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from apps.accounts.models import User, Contact


class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'email', 'is_account_id', 'is_active', 'created_on')
    list_filter = ('is_account_id', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_on',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject', 'message', 'created_on')
    list_filter = ('created_on', )
    search_fields = ('email', 'subject')
    ordering = ('-created_on',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(User, UserAdmin)
