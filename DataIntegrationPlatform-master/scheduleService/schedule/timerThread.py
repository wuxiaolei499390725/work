"""
author wanghaiying
date 20190601
description 定时器线程
"""
from schedule.threadBase import ThreadBase


class TimerThread(ThreadBase):
    def __init__(self, value, work_event=None, complete_event=None):
        # super().__init__()
        self._interval = value
        ThreadBase.__init__(self, work_event, complete_event)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    def thread_proc(self):
        pass

    def run(self):
        print("TimerThread run ....")
