from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        DRIVER = _('D'), _('DRIVER')
        GUEST = _('G'), _('GUEST')
    role = models.CharField(max_length=1, choices=RoleChoice.choices, default='G', verbose_name='User role')


class DriverProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name=_('User'))
    first_name = models.CharField(max_length=100, verbose_name=_('Driver firstname'))
    last_name = models.CharField(max_length=100, verbose_name=_('Driver lastname'))
    driving_license = models.ManyToManyField('car_delivery.DrivingLicense', verbose_name=_('Driving license'))
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
