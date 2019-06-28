"""
author wanghaiying
date 20190601
description 任务重试策略
"""


class ErrorRetryPolicy(object):
    max_error_count = 5
    max_retry_interval = 60  # minute
    retry_interval_factor = 10  # minute

    def __init__(self, task):
        self.task = task

    @property
    def max_error_count(self):
        return self.max_error_count

    @max_error_count.setter
    def max_error_count(self, value):
        self.max_error_count = value

    @property
    def max_retry_interval(self):
        return self.max_retry_interval

    @max_retry_interval.setter
    def max_retry_interval(self, value):
        pass

    @property
    def retry_interval_factor(self):
        return self.retry_interval_factor

    @retry_interval_factor.setter
    def retry_interval_factor(self, value):
        self.retry_interval_factor = value

    def can_retry_now(self):
        # TODO
        return True
