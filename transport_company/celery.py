import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_company.settings')

app = Celery('transport_company')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'car_delivery.tasks.notify_driver_upcoming_race',
        'schedule': crontab(minute=0, hour='*/3'),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
