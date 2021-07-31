from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class RaceCreationValidator:
    """Race objects creating validator."""
    def __init__(self, data: dict):
        self.vehicle = data.get('vehicle')
        self.driver = data.get('driver')
        self.pickup_time = data.get('pickup_time')
        self.supply_time = data.get('supply_time')

    def check_limit_availability(self) -> None:
        drivers_current_time_count = 0
        for race in self.vehicle.race_set.all():
            if race.supply_time >= datetime.strptime(self.supply_time, '%Y-%m-%d %H:%M:%S') <= race.supply_time and \
                    race.pickup_time >= datetime.strptime(self.pickup_time, '%Y-%m-%d %H:%M:%S') <= race.pickup_time:
                drivers_current_time_count += 1
        if self.vehicle.drivers_limit <= drivers_current_time_count:
            raise serializers.ValidationError(_("This car has reached max drivers limit."))

    def check_driver_busy(self) -> None:
        race_list = [race for race in self.driver.race_set.all()]
        for race in race_list:
            if race.supply_time >= datetime.strptime(self.pickup_time, '%Y-%m-%d %H:%M:%S'):
                raise serializers.ValidationError(_("This driver already has race at this time."))

    def check_driving_category(self) -> None:
        if self.vehicle.driving_category not in self.driver.get_license_list:
            raise serializers.ValidationError(_("Driver has not required driving license."))

    def check_all(self) -> None:
        self.check_limit_availability()
        self.check_driver_busy()
        self.check_driving_category()
