from celery import Celery

app = Celery('web_app_project')
app.autodiscover_tasks()