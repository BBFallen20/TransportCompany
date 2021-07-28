from rest_framework import serializers

from car_delivery.models import Race, Vehicle


class RaceCreationValidator:
    def __init__(self, data: dict):
        self.vehicle = data.get('vehicle')
        self.driver = data.get('driver')
        self.pickup_time = data.get('pickup_time')

    def check_limit_availability(self):
        if self.vehicle.drivers_limit <= self.vehicle.get_drivers_count():
            raise serializers.ValidationError("This car has reached max drivers limit.")

    def check_driver_busy(self):
        race_list = [race for race in self.driver.race_set.all()]
        for race in race_list:
            if race.supply_time >= self.pickup_time:
                raise serializers.ValidationError("This driver already has race at this time.")

    def check_driving_category(self):
        if self.vehicle.driving_category not in self.driver.get_license_list():
            raise serializers.ValidationError("Driver has not required driving license.")

    def check_all(self):
        self.check_driver_busy()
        self.check_limit_availability()
        self.check_driving_category()


def update_vehicle_status(vehicle_id):
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
    if vehicle:
        if not vehicle.using:
            vehicle.using = True
            vehicle.save()
