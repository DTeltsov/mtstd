from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from music.models import Song

from .models import AccountUser, Subscription


class SongInline(admin.TabularInline):
    model = Song.users.through
    extra = 1


class AccountAdminUser(UserAdmin):
    list_display = (*UserAdmin.list_display, 'subscription_model', )
    list_select_related = ('subscription_model', )
    inlines = [SongInline]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', "last_name", 'username', 'password1', 'password2', 'subscription_model', ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Subscription Information', {'fields': ('subscription_model',)}),
    )


admin.site.register(AccountUser, AccountAdminUser)
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Admin Panel"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
