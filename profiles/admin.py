from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.contrib.auth import get_user_model


class UserProfileInline(admin.StackedInline):
    model = Profile


class NewUserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), NewUserAdmin)
