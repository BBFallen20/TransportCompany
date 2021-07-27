from rest_framework import serializers


class VehicleDriverService:
    def __init__(self, vehicle, driver):
        self.vehicle = vehicle
        self.driver = driver

    def check_vehicle_drivers_limit_availability(self):
        if self.vehicle.drivers_limit >= self.vehicle.get_drivers_count():
            return True
        raise serializers.ValidationError("This car has reached max drivers limit.")

    def check_vehicle_driver_already_set(self):
        if self.driver not in [vehicle_driver.driver for vehicle_driver in self.vehicle.vehicledriver_set.all()]:
            return True
        raise serializers.ValidationError("This driver already assigned to this vehicle.")

    def check_vehicle_driver_driving_category(self):
        if self.vehicle.driving_category in self.driver.get_license_list():
            return True
        raise serializers.ValidationError("Driver has not required driving license.")

    def check_all(self):
        self.check_vehicle_driver_driving_category()
        self.check_vehicle_driver_already_set()
        self.check_vehicle_drivers_limit_availability()
