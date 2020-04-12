from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_login', 'date_joined',
                    'is_admin', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
