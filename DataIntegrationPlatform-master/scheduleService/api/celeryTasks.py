"""
author wanghaiying
date 20190601
description celery任务定义
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task


@task(bind=True)
@shared_task
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@task(bind=True, autoretry_for=(Exception,), task_reject_on_worker_lost=True)
def add(self, x, y):
    return x + y


@task(bind=True, autoretry_for=(Exception,), task_reject_on_worker_lost=True)
def substract(self, x, y):
    return x - y


if __name__ == '__main__':
    task_id = add.apply_async(args=[1,3])
    print(task_id)
