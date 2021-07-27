from django.contrib import admin
from .models import Vehicle, Driver, DrivingLicense, VehicleDriver


class VehicleDriverInline(admin.StackedInline):
    model = VehicleDriver
    fields = ['driver']
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [VehicleDriverInline]
    readonly_fields = ['using']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    pass



