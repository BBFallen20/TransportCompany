web: gunicorn transport_company.wsgi --log-file -
celery: celery worker -A transport_company -l info -c 4