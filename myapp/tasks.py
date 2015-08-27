from example import app
from celery import Celery

celery = Celery('example.tasks')
celery.conf.update(app.config)

@celery.task(ignore_result=True)
def resize_uploaded_image(filename, w, h):
    # ...
