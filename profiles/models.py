from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        DRIVER = _('D'), _('DRIVER')
        GUEST = _('G'), _('GUEST')

    role = models.CharField(max_length=1, choices=RoleChoice.choices, default='G', verbose_name='User role')

    REQUIRED_FIELDS = ['email', 'role']


class ProfileComment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('Comment user'))
    # GenericForeignKey relation to universal profile using.
    comment_profile = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label='profiles', model='driverprofile')
    )
    profile_id = models.PositiveIntegerField()
    profile = GenericForeignKey('comment_profile', 'profile_id')

    content = models.TextField(max_length=1500, verbose_name=_('Comment text'))
    muted = models.BooleanField(default=False, verbose_name=_('Comment mute flag'))
    # Comment reply logic
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('Parent comment')
    )

    @property
    def child_list(self):
        return ProfileComment.objects.filter(parent_comment=self)

    @property
    def is_parent(self):
        return True if self.parent_comment is not None else False


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
    comments = GenericRelation('ProfileComment', content_type_field='comment_profile', object_id_field='profile_id')

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
