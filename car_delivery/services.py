from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from car_delivery.models import Race, Vehicle


class RaceCreationValidator:
    """Race objects creating validator. C"""
    def __init__(self, data: dict):
        self.vehicle = data.get('vehicle')
        self.driver = data.get('driver')
        self.pickup_time = data.get('pickup_time')

    def check_limit_availability(self) -> None:
        if self.vehicle.drivers_limit <= self.vehicle.get_drivers_count:
            raise serializers.ValidationError(_("This car has reached max drivers limit."))

    def check_driver_busy(self) -> None:
        race_list = [race for race in self.driver.race_set.all()]
        for race in race_list:
            if race.supply_time >= self.pickup_time:
                raise serializers.ValidationError(_("This driver already has race at this time."))

    def check_driving_category(self) -> None:
        if self.vehicle.driving_category not in self.driver.get_license_list:
            raise serializers.ValidationError(_("Driver has not required driving license."))

    def check_all(self) -> None:
        self.check_driver_busy()
        self.check_limit_availability()
        self.check_driving_category()


@receiver(pre_delete, sender=Race)
@receiver(post_save, sender=Race)
def update_vehicle_status(sender, instance, **kwargs) -> None:
    vehicle = Vehicle.objects.filter(id=instance.vehicle.id).first()
    if vehicle:
        race_list = Race.objects.filter(vehicle_id=vehicle.id)
        vehicle.using = True if not vehicle.using and race_list else False
        vehicle.save()
