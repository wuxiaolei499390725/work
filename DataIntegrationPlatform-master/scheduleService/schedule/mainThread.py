"""
author wanghaiying
date 20190601
description 主调度线程
"""
from threading import Event
import traceback

from schedule.errorRetryPolicy import ErrorRetryPolicy
from schedule.idleTime import IdleTime
from schedule.manageTaskStatus import ManageTaskStatus
from schedule.metadataValidator import MetadataValidator
from schedule.preCondition import PreCondition
from schedule.manageSchedule import Schedule
from schedule.task import TaskType
from schedule.taskList import TaskList
from schedule.taskWorker import TaskWorker
from schedule.taskWorkerPool import TaskWorkerPool
from schedule.threadBase import ThreadBase
from schedule.timerThread import TimerThread


def check_pre_condition(task):
    # 判断前置条件
    condition = PreCondition().create(task)
    if not condition.is_true():
        return False
    # 错误重试策略
    erp = ErrorRetryPolicy(task=task)
    if not erp.can_retry_now():
        return False
    # 判断元数据
    meta = MetadataValidator(task=task)
    if not meta.validate():
        # 改变状态
        task.update_validate_error(meta.error_info)
        return False
    return True


def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@Singleton
class MainThread(ThreadBase):
    def __init__(self, task_worker_pool=None, task_list=None, stop_flag=False, timer_thread=None,
                 manage_task_status=None, work_event=Event(), complete_event=Event()):
        self._task_worker_pool = task_worker_pool
        self._task_list = task_list
        self._task_list.load_from_db()
        self._stop_flag = stop_flag
        self._timer_thread = timer_thread
        self._manage_task_status = manage_task_status
        manage_task_status.clear_task_status()

        self._threads = list()
        self._events = list()

        i = 0
        if len(self._task_worker_pool.running_workers) > 0:
            while i < self._task_worker_pool.capacity:
                running_worker = self._task_worker_pool.running_workers[i]
                self._threads.append(running_worker)
                self._events.append(running_worker.complete_event)
                i += 1
        # add timer thread
        self._threads.append(self._timer_thread)
        self._events.append(self._timer_thread.complete_event)
        # add main thread
        self._threads.append(self)

        ThreadBase.__init__(self, work_event, complete_event)
        self._events.append(self.complete_event)

    @property
    def events(self):
        return self._events

    @property
    def stop_flag(self):
        return self._stop_flag

    def run(self):
        self._timer_thread.run()
        self._task_worker_pool.run()

    def clean(self):
        # 是否需要lock
        self._stop_flag = True
        self.complete_event.set()
        self._task_worker_pool.clean()
        # wait for main thread exit
        self.own_thread.join()

    def thread_proc(self):
        i = 0
        if len(self.events) > 0:
            while (not self.stop_flag or not self._task_worker_pool.all_task_complete) and i < len(self.events):
                print("thread_proc while" + str(i))
                self.event_handler(i)
                i += 1

    def event_handler(self, i):
        thread = self._threads[i]
        # if isinstance(thread, TaskWorker):
        #     self.on_task_complete(thread)
        if not self._stop_flag:
            self.loop_dispatch(i)

    def loop_dispatch(self, i):
        print(" loop_dispatch " + str(i))
        while self.dispatch_task(i):
            pass

    def dispatch_task(self, i):
        print("     dispatch_task " + str(i))

        # 是否有待分配任务
        task = self._task_list.current_task()
        if task is None:
            return False

        # 是否有空闲worker
        print("     has_idle_worker", self._task_worker_pool.has_idle_worker)
        if not self._task_worker_pool.has_idle_worker:
            return False

        # 只有DSA和LOOP任务才需要判断空闲时间
        # if task.task_type in (TaskType.DSA, TaskType.LOOP):
        #     # 是否交易空闲时间
        #     if not IdleTime().is_idle_time(now):
        #         self._task_list.next()
        #         return True
        # 从调度时间表获取执行日期
        # sh = Schedule().create(task.schedule_type)
        # date_id = sh.get_excute_date_id(task, now)
        # if date_id <= 0:
        #     self._task_list.next()
        #     return True
        # task._current_execute_date_id = date_id
        # 判断前置条件
        # if not check_pre_condition(task):
        #     self._task_list.next()
        #     return True
        # 写日志. log before run task
        # task.insert_log()

        # link Task & Thread
        idle_worker = self._task_worker_pool.get_idle_worker()
        task.task_worker = idle_worker
        idle_worker.task = task
        self._task_list.next()

        # idle_worker添加到running_workers数组里
        self._task_worker_pool.running_workers.append(idle_worker)

        # 执行任务. run task
        idle_worker.execute_task()
        return True

    def on_task_complete(self, task_worker):
        if task_worker.task is not None:
            # update log
            task_worker.task.update_log()
            # Separate task & thread
            task_worker.task.task_worker = None
            task_worker.task = None
        self._task_worker_pool.recovery_worker(task_worker)


if __name__ == '__main__':
    mainThread = MainThread(task_worker_pool=TaskWorkerPool(), task_list=TaskList(local_ip='127.0.0.1'),
                            timer_thread=TimerThread(value=3, work_event=Event(), complete_event=Event()),
                            manage_task_status=ManageTaskStatus())
    # try:
    #     # mainThread.run()
    #     # mainThread.clean()
    #
    #     task_worker_pool = TaskWorkerPool()
    # except Exception as e:
    #     print(traceback.format_exc(), e)
