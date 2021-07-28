from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Vehicle(models.Model):
    model = models.CharField(max_length=100, verbose_name=_('Vehicle model title'))
    mark = models.CharField(max_length=100, verbose_name=_('Vehicle mark title'))
    driving_category = models.ForeignKey(
        'DrivingLicense',
        on_delete=models.CASCADE,
        verbose_name=_('Required driving category')
    )
    using = models.BooleanField(default=False, editable=False, verbose_name=_('Vehicle in use flag'))
    drivers_limit = models.PositiveSmallIntegerField(default=1, verbose_name=_('Vehicle drivers limit'))

    def __str__(self) -> str:
        return f"Car#{self.id} - {self.mark} {self.model} Category: {self.driving_category}."

    def __repr__(self) -> str:
        return f"Car({self.id} - {self.mark} {self.model})"

    @property
    def get_drivers_count(self) -> int:
        return len(set(list(map(lambda x: x.driver, self.race_set.all()))))

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')


class Race(models.Model):
    class RaceChoice(models.TextChoices):
        STARTED = _('S'), _('STARTED')
        PENDING = _('P'), _('PENDING')
        ENDED = _('E'), _('ENDED')
        CANCELED = _('C'), _('CANCELED')
    vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.CASCADE,
        related_query_name='vehicle_vehicle_driver',
        verbose_name=_('Vehicle')
    )
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.CASCADE,
        related_query_name='driver_vehicle_driver',
        verbose_name=_('Driver')
    )
    pickup_time = models.DateTimeField(verbose_name=_('Race start date and time'))
    supply_time = models.DateTimeField(verbose_name=_('Race end date and time'))
    pickup_location = models.CharField(max_length=300, verbose_name=_('Race products pickup location'))
    supply_location = models.CharField(max_length=300, verbose_name=_('Race products supply location'))
    status = models.CharField(max_length=1, choices=RaceChoice.choices, default='P', verbose_name=_('Race status'))

    @staticmethod
    def get_available_vehicles(self) -> Vehicle:
        return Vehicle.objects.filter(using=False)

    def __str__(self) -> str:
        return f"Race#{self.id} {self.status} {self.pickup_time}-{self.supply_time}"

    def __repr__(self) -> str:
        return f"Race(id:{self.id} {self.status} {self.pickup_time}-{self.supply_time})"

    class Meta:
        verbose_name = _('Race')
        verbose_name_plural = _('Races')


class Driver(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('Driver firstname'))
    last_name = models.CharField(max_length=100, verbose_name=_('Driver lastname'))
    driving_license = models.ManyToManyField('DrivingLicense', verbose_name=_('Driving license'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        default=0,
        verbose_name=_('Driver rating(0-100 where 100 is max rating)'),
    )

    def __str__(self) -> str:
        return f"Driver#{self.id} {self.first_name} {self.last_name} " \
               f"Categories: {','.join(map(lambda x: x.title, self.get_license_list))}."

    def __repr__(self) -> str:
        return f"Driver({self.first_name} {self.last_name})"

    @property
    def get_license_list(self) -> list:
        return [driver_license for driver_license in self.driving_license.all()]

    class Meta:
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')


class DrivingLicense(models.Model):
    title = models.CharField(max_length=10, verbose_name=_('License title'))

    def __str__(self) -> str:
        return f"License {self.title}"

    def __repr__(self) -> str:
        return f"License({self.id} {self.title})"

    class Meta:
        verbose_name = _('Driving license')
        verbose_name_plural = _('Driving licenses')
