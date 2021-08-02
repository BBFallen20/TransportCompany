import csv
from datetime import datetime
from functools import wraps

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions


class RaceCreationValidator:
    """Race objects creating validator."""

    def __init__(self, data: dict):
        self.vehicle = data.get('vehicle')
        self.driver = data.get('driver')
        self.pickup_time = data.get('pickup_time')
        self.supply_time = data.get('supply_time')

    def get_vehicle_drivers_limit(self):
        return self.vehicle.drivers_limit

    def check_limit_availability(self) -> None:
        drivers_current_time_count = 0
        for race in self.vehicle.race_set.all():
            if race.supply_time >= datetime.strptime(self.supply_time, '%Y-%m-%d %H:%M:%S') <= race.supply_time and \
                    race.pickup_time >= datetime.strptime(self.pickup_time, '%Y-%m-%d %H:%M:%S') <= race.pickup_time:
                drivers_current_time_count += 1
        if self.get_vehicle_drivers_limit() <= drivers_current_time_count:
            raise exceptions.ValidationError(_("This car has reached max drivers limit."))

    def get_drivers_race_list(self):
        return [race for race in self.driver.race_set.all()]

    def check_driver_busy(self) -> None:
        race_list = self.get_drivers_race_list()
        for race in race_list:
            if race.supply_time >= datetime.strptime(self.pickup_time, '%Y-%m-%d %H:%M:%S'):
                raise exceptions.ValidationError(_("This driver already has race at this time."))

    def get_vehicle_driving_category(self):
        return self.vehicle.driving_category

    def check_driving_category(self) -> None:
        if self.get_vehicle_driving_category() not in self.driver.license_list:
            raise exceptions.ValidationError(_("Driver has not required driving license."))

    def check_all(self) -> None:
        self.check_limit_availability()
        self.check_driver_busy()
        self.check_driving_category()


def get_races_csv(queryset):
    output = []
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Driver', 'Vehicle', 'Supply time', 'Pickup time', 'Supply location', 'Pickup location', 'Status'])
    for race in queryset:
        output.append(
            [
                race.driver,
                race.vehicle,
                race.supply_time,
                race.pickup_time,
                race.supply_location,
                race.pickup_location,
                race.status
            ]
        )
    writer.writerows(output)
    return response


def csv_exportable(f):
    @wraps(f)
    def wrapper(self, *args, **kw):
        if 'export' not in self.request.get_full_path():
            return f(self, *args, **kw)
        return get_races_csv(self.get_queryset())
    return wrapper

