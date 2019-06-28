"""
author wanghaiying
date 20190601
description 任务队列
"""
import datetime
from schedule.manageTaskStatus import ManageTaskStatus, get_local_task
from schedule.timerThread import TimerThread


class TaskList(object):
    def __init__(self, last_load_time=datetime.datetime(1900, 1, 1), current_index=0, tasks=None, local_ip=None):
        print("task list init")
        self._last_load_time = last_load_time
        self._current_index = current_index
        self._tasks = tasks
        self._local_ip = local_ip

    @property
    def is_time_to_refresh(self):
        # TODO
        return True
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') - self._last_load_time
        return ts.seconds >= TimerThread.interval

    def load_from_db(self):
        if not self.is_time_to_refresh:
            return
        mts = ManageTaskStatus()
        self._tasks = get_local_task(self._local_ip)
        self._last_load_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def contains_task(self, task_id):
        i = 0
        while i < self._current_index:
            task = self._tasks[i]
            if task.task_id == task_id:
                return True
            i += 1
        return False

    def current_task(self):
        if self._current_index < 0 or self._current_index >= len(self._tasks):
            return None
        return self._tasks[self._current_index]

    def next(self):
        if self._current_index >= 0:
            self._current_index += 1
