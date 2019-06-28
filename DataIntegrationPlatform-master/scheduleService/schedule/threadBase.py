"""
author wanghaiying
date 20190601
description 任务线程父类
"""
from threading import Event, Thread
from abc import abstractmethod, ABCMeta


# class ThreadBase(metaclass=ABCMeta):
class ThreadBase(object):
    def __init__(self, work_event, complete_event):
        self._work_event = work_event
        # print(self.__class__)
        # print("threadBase work_base:")
        # print(self._work_event)
        self._complete_event = complete_event
        self._own_thread = Thread(self.thread_proc())

    @property
    def work_event(self):
        return self._work_event

    @property
    def complete_event(self):
        return self._complete_event

    @property
    def own_thread(self):
        return self._own_thread

    @abstractmethod
    def thread_proc(self):
        pass

    def run(self):
        self._own_thread.start()
