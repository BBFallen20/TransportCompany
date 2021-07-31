from django.contrib import admin

from .models import Vehicle, DrivingLicense, Race


class RaceInline(admin.StackedInline):
    model = Race
    fields = ['driver', 'supply_time', 'pickup_time', 'status', 'supply_location', 'pickup_location']
    extra = 1


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [RaceInline]


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    pass
