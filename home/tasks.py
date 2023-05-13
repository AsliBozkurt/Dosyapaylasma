import time

from celery import shared_task


@shared_task(name="hello")
def hello():
    i = 1
    while i <= 10:
        time.sleep(1)
        print(i)
        i += 1

    return "success"
