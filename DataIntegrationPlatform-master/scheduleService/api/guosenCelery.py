"""
author wanghaiying
date 20190601
description celery调度对象定义
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import shared_task, task

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', './scheduleService.settings')

# app = Celery('scheduleService', broker='amqp://guest:guest@localhost:5672', backend='amqp://guest:guest@localhost:5672')
app = Celery('scheduleService', broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/1")


# We also add the Django settings module as a configuration source for Celery. This means that you don’t have to use multiple configuration files,
# and instead configure Celery directly from the Django settings; but you can also separate them if wanted.

# Using a string here means the worker don't have to serialize the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks('api')


@app.task(bind=True, autoretry_for=(Exception,), task_reject_on_worker_lost=True)
# @shared_task
def add(self, x, y):
    return x + y


@app.task(bind=True, autoretry_for=(Exception,), task_reject_on_worker_lost=True)
def substract(self, x, y):
    return x - y
