web: gunicorn transport_company.wsgi --log-file -
celery: celery -A transport_company worker
beat: celery worker --loglevel=info --beat