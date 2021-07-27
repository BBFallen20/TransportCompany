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

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(VehicleAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(VehicleAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        drivers = VehicleDriver.objects.filter(vehicle=obj.id)
        obj.using = True if drivers else False
        obj.save()
        return obj


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    pass



