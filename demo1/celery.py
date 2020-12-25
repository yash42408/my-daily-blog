
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab



# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo1.settings')

app = Celery('demo1')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'blog.tasks.make_blogger',
        'schedule': 30.0,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}
app.conf.timezone = 'UTC'
