from django.contrib.auth.models import User
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
    drivers_limit = models.PositiveSmallIntegerField(default=1, verbose_name=_('Vehicle drivers limit'))

    def __str__(self) -> str:
        return f"Car#{self.id} - {self.mark} {self.model} Category: {self.driving_category}."

    def __repr__(self) -> str:
        return f"Car({self.id} - {self.mark} {self.model})"

    @property
    def drivers_count(self) -> int:
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
        'profiles.DriverProfile',
        on_delete=models.CASCADE,
        related_query_name='driver_vehicle_driver',
        verbose_name=_('Driver')
    )
    pickup_time = models.DateTimeField(verbose_name=_('Race start date and time'))
    supply_time = models.DateTimeField(verbose_name=_('Race end date and time'))
    pickup_location = models.CharField(max_length=300, verbose_name=_('Race products pickup location'))
    supply_location = models.CharField(max_length=300, verbose_name=_('Race products supply location'))
    status = models.CharField(max_length=1, choices=RaceChoice.choices, default='P', verbose_name=_('Race status'))

    def __str__(self) -> str:
        return f"Race#{self.id} {self.status} {self.pickup_time}-{self.supply_time}"

    def __repr__(self) -> str:
        return f"Race(id:{self.id} {self.status} {self.pickup_time}-{self.supply_time})"

    class Meta:
        verbose_name = _('Race')
        verbose_name_plural = _('Races')


class DrivingLicense(models.Model):
    title = models.CharField(max_length=10, verbose_name=_('License title'), unique=True)

    def __str__(self) -> str:
        return f"License {self.title}"

    def __repr__(self) -> str:
        return f"License({self.id} {self.title})"

    class Meta:
        verbose_name = _('Driving license')
        verbose_name_plural = _('Driving licenses')
