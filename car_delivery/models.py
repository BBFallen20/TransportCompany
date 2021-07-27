from django.db import models


class Vehicle(models.Model):
    model = models.CharField(max_length=100, verbose_name='Vehicle model title')
    mark = models.CharField(max_length=100, verbose_name='Vehicle mark title')
    driving_category = models.ForeignKey(
        'DrivingLicense',
        on_delete=models.CASCADE,
        verbose_name='Required driving category'
    )
    using = models.BooleanField(default=False, editable=False, verbose_name='Vehicle in use flag')
    drivers_limit = models.PositiveSmallIntegerField(verbose_name='Vehicle drivers limit', default=1)

    def __str__(self) -> str:
        return f"Car#{self.id} - {self.mark} {self.model} Category: {self.driving_category}."

    def __repr__(self):
        return f"Car({self.id} - {self.mark} {self.model})"

    def save(self, *args, **kwargs):
        super(Vehicle, self).save(*args, **kwargs)
        drivers = VehicleDriver.objects.filter(vehicle_id=self.id)
        self.using = True if drivers else False
        return super(Vehicle, self).save(*args, **kwargs)

    def get_drivers_count(self):
        return self.vehicledriver_set.count()


class VehicleDriver(models.Model):
    vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.CASCADE,
        verbose_name='Vehicle',
        related_query_name='vehicle_vehicle_driver'
    )
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.CASCADE,
        verbose_name='Driver',
        related_query_name='driver_vehicle_driver'
    )

    @staticmethod
    def get_available_vehicles(self):
        return Vehicle.objects.filter(using=False)

    def save(self, *args, **kwargs):
        super(VehicleDriver, self).save(*args, **kwargs)
        self.vehicle.using = True
        self.vehicle.save()


class Driver(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Driver firstname')
    last_name = models.CharField(max_length=100, verbose_name='Driver lastname')
    driving_license = models.ManyToManyField('DrivingLicense', verbose_name='Driving license')

    def __str__(self) -> str:
        return f"Driver#{self.id} {self.first_name} {self.last_name} " \
               f"Categories: {[category.title for category in self.driving_license.all()]}."

    def __repr__(self) -> str:
        return f"Driver({self.first_name} {self.last_name})"

    def get_license_list(self):
        return [driver_license for driver_license in self.driving_license.all()]

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'


class DrivingLicense(models.Model):
    title = models.CharField(max_length=10, verbose_name='License title')

    def __str__(self) -> str:
        return f"License {self.title}"

    def __repr__(self) -> str:
        return f"License({self.id} {self.title})"

    class Meta:
        verbose_name = 'Driving license'
        verbose_name_plural = 'Driving licenses'
