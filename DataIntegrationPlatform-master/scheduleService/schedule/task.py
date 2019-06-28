"""
author wanghaiying
date 20190601
description task实体类
"""
import datetime
from enum import Enum

from api.guosenCelery import *


class Task:
    def __init__(self, task_id=None, task_name=None, execution_type=None, task_type=None, schedule_type=None,
                 pre_condition_type=None, execution_expression=None, start_execute_date_id=None,
                 current_execute_date_id=None,
                 last_succeeded_execute_date_id=None, error_count=None, last_start_time=None, is_reload=False,
                 start_time=None, complete_time=None, error_info=None, is_success=None, task_log_id=None,
                 task_worker=None, task_log_writer=None):
        self.task_id = task_id
        self._task_name = task_name
        self._execution_type = execution_type
        self._task_type = task_type
        self._schedule_type = schedule_type
        self._pre_condition_type = pre_condition_type
        self._execution_expression = execution_expression
        self._start_execute_date_id = start_execute_date_id
        self._current_execute_date_id = current_execute_date_id
        self._last_succeeded_execute_date_id = last_succeeded_execute_date_id
        self._error_count = error_count
        self._last_start_time = last_start_time
        self._is_reload = is_reload
        self._start_time = start_time
        self._complete_time = complete_time
        self._error_info = error_info
        self._is_success = is_success
        self._task_log_id = task_log_id
        self._task_worker = task_worker
        self._task_log_writer = task_log_writer

    @property
    def pre_condition_type(self):
        return self._pre_condition_type

    @property
    def schedule_type(self):
        return self._schedule_type

    @property
    def task_type(self):
        return self._task_type

    @property
    def current_execute_date_id(self):
        return self._current_execute_date_id

    @property
    def task_worker(self):
        return self._task_worker

    @task_worker.setter
    def task_worker(self, value):
        self._task_worker = value

    @property
    def task_log_writer(self):
        return self._task_log_writer

    # @staticmethod
    # def create(self, dr):
    #     task = Task()
    #     # task._task_log_writer = self._task_log_writer.create(task, dr)
    #     return task

    def insert_log(self):
        self._start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._task_log_id = self._task_log_writer.insert_log()

    def update_log(self):
        sql = ""
        self._task_log_writer.update_log(sql)

    def execute(self):
        try:
            celery_task = self._execution_expression
            print("celery_task:"+celery_task)
            if celery_task is not None:
                celery_async_result = app.send_task("guosenCelery.%s" % celery_task, args=(1, 2))
                if celery_async_result.successful():
                    self._is_success = True
                else:
                    self._is_success = False
        except Exception as e:
            self._is_success = False
            self._error_info = e.Message
        finally:
            self._is_success = True
            self._complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return celery_async_result

    def update_validate_error(self, error):
        self._start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._complete_time = self._start_time
        self._error_info = error
        # self._task_log_writer.UpdateValidateError()


class TaskType(Enum):
    DSA = "DSA"  # 检查系统标志位,采集任务，ETL的 E的部分，从源系统采集数据到 数据中心的任务就属于这个分组
    DW = "DW"  # 数据仓库的任务，一般是 ETL的 T的部分，主要是包括 清洗，转换，整合数据的 任务
    ST = "ST"  # ST 一般是统计分析的任务，用于计算、统计各种指标，很多业务逻辑的任务就放在ST的这个组中
    LOOP = "LOOP"  # 一般要反复检查时间和源系统的标志位；这类任务一般只有时间到了，或者标志位ok了，他们才会成功；
    # 没到时间或者标志位状态不对，会认为任务失败，然后经过一定间隔后再次调度
    IFC = "IFC"  # 推送数据到其他应用, 数据中心的数据 推送向 其他应用的数据库
    OTHER = "OTHER"
