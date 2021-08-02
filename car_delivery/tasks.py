import datetime

from django.core.mail import send_mail
from django.template import Template, Context

from car_delivery.models import Race
from transport_company.celery import app
from transport_company.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

REPORT_TEMPLATE = """
Hi there, {{ username }}!
You have upcoming race at: {{ race_time }} 
Pickup location: {{ pickup_location }}.
"""


@app.task
def notify_driver_upcoming_race():
    template = Template(REPORT_TEMPLATE)
    races = Race.objects.filter(status='P')
    for race in races:
        if datetime.datetime.now().hour - race.pickup_time.hour <= 4:
            send_mail(
                subject='TransportCompany',
                message=template.render(context=Context(
                    {
                        'username': race.driver.user.email,
                        'race_time': race.pickup_time,
                        'pickup_location': race.pickup_location
                    }
                )),
                from_email=EMAIL_HOST_USER,
                recipient_list=[race.driver.user.email],
                auth_user=EMAIL_HOST_USER,
                auth_password=EMAIL_HOST_PASSWORD,
                fail_silently=False,
            )
