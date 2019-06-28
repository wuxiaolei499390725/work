"""
author wanghaiying
date 20190601
description 任务执行者
"""
from threading import Thread, Event
from schedule.task import Task
from schedule.threadBase import ThreadBase


class TaskWorker(ThreadBase):
    def __init__(self, task=None, task_id=None, stop_flag=False, async_result=None, work_event=None,
                 complete_event=None):
        self._task = task
        self._stop_flag = stop_flag
        self._own_thread = Thread(name="TaskWorker")
        self.name = "TaskWorker"
        ThreadBase.__init__(self, work_event, complete_event)
        self._task_id = task_id
        self._async_result = async_result

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        self._task = value

    @property
    def task_id(self):
        return self._task_id

    @property
    def async_result(self):
        return self._async_result

    def execute_task(self):
        if self._task is not None:
            print("execute_task()")
            try:
                self._async_result = self._task.execute()
                self._task_id = self._async_result.id
                print("_task_id:" + self._task_id)
            except Exception as e:
                print(e)

    def thread_proc(self):
        while not self._stop_flag:
            self.work_event.wait()
            self.execute_task()
            self.complete_event.set()
            # print("TaskWorker work_event is_set:" + str(self.work_event.is_set()))
            # print("TaskWorker complete_event is_set:" + str(self.complete_event.is_set()))
            # time.sleep(5)

    def run(self):
        self.work_event().set()


if __name__ == '__main__':
    # task = Task()
    # task_worker = TaskWorker()
    task_worker = TaskWorker(task=None, task_id=None, async_result=None, work_event=Event(), complete_event=Event())
    print(task_worker.complete_event)
    print(task_worker.work_event)
    print(task_worker.own_thread)

# print(task_worker._task)
