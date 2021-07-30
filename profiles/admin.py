from django.contrib import admin

from .models import User, DriverProfile, ProfileComment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(DriverProfile)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileComment)
class DriverProfileComment(admin.ModelAdmin):
    pass
