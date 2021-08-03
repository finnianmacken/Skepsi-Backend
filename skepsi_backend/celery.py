import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skepsi_backend.settings')

app = Celery('skepsi_app')
app.config_from_object('django.conf:settings')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
