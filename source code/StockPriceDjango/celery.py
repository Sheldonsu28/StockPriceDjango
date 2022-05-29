import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StockPriceDjango.settings')
app = Celery('StockPriceDjango')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_workday_from_9_to_5': {
        'task': 'Email.tasks.send_email',
        'schedule': crontab(
            day_of_week='mon,tue,wed,thu,fri',
            hour='9-17',
            minute=0
        )
    }
}

app.conf.task_ignore_result = False


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
