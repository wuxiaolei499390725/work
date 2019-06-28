"""
author wanghaiying
date 20190601
description 任务队列池
"""
from queue import Queue
from threading import Event

from schedule.taskWorker import TaskWorker
from schedule.threadBase import ThreadBase


class TaskWorkerPool(ThreadBase):
    def __init__(self, capacity=2, stop_flag=False, task_id=None):
        self.capacity = capacity  # 根据celery的配置动态调整
        self._stop_flag = stop_flag
        self._running_workers = list()
        self._running_workers.append(TaskWorker(work_event=Event(), complete_event=Event()))
        self._running_workers.append(TaskWorker(work_event=Event(), complete_event=Event()))
        self._idle_workers = Queue()
        for i in range(0, self.capacity):
            worker = TaskWorker()
            self._idle_workers.put(worker)
        self.name = "TaskWorkerPoolThread"
        # ThreadBase.__init__(self, work_event, complete_event)
        print("TaskWorkerPool work_base:")
        # print(self.work_event)
        self._task_id = task_id

    @property
    def stop_flag(self):
        return self._stop_flag

    @property
    def running_workers(self):
        return self._running_workers

    @property
    def idle_workers(self):
        return self._idle_workers

    @property
    def all_task_complete(self):
        return self.idle_workers.qsize() == self.capacity

    @property
    def has_idle_worker(self):
        # print("idle_workers qsize:" + str(self.idle_workers.qsize()))
        return self.idle_workers.qsize() > 0

    def clean(self):
        self._stop_flag = True
        self._work_event.set()

    def get_idle_worker(self):
        if 0 == self.idle_workers.qsize():
            return None
        task_worker = self.idle_workers.get()
        # self.running_workers.remove(task_worker)
        return task_worker

    # def recovery_worker(self, task_worker):
    #     self.idle_workers.put(task_worker)

    def thread_proc(self):
        while not self.stop_flag:
            # self._work_event.wait()
            # 检查异步任务有没有完成的
            for running_worker in self.running_workers:
                if running_worker.async_result.successful():
                    running_worker.complete_event.set()
                    # 若有worker完成了任务,需要从running_worker中移出,并重新加入idle_workers
                    self._running_workers.remove(running_worker)
                    self.idle_workers.put(running_worker)

    # def run(self):
    #     print("TaskWorkerPool run ....")
    #     super.work_event.set()
    #     task_worker = self._idle_workers.get()
    #     # print(" TaskWorkerPool work_event is_set:" + str(task_worker.work_event.is_set()))
    #     task_worker.work_event.set()
    #     # print(" TaskWorkerPool work_event is_set:" + str(task_worker.work_event.is_set()))


if __name__ == '__main__':
    taskWorkerPool = TaskWorkerPool()
    # print(taskWorkerPool.work_event)
    # print(taskWorkerPool.complete_event)
    # idle_worker = taskWorkerPool.get_idle_worker()
    # time.sleep(3)
    # taskWorkerPool.run()