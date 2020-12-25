from celery import shared_task
from .models import User
from demo1.celery import app



@app.task
def make_blogger():
    for user in User.objects.all():
        if user.is_request:
            user.is_blogger=True
            user.save()
    

