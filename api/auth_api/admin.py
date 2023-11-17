from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountUser


class AccountAdminUser(UserAdmin):
    list_display = (*UserAdmin.list_display, 'subscription_model', )
    list_select_related = ('subscription_model',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', "last_name", 'username', 'password1', 'password2',),
        }),
    )


admin.site.register(AccountUser, AccountAdminUser)
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Admin Panel"
