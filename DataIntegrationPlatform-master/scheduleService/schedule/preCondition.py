"""
author wanghaiying
date 20190601
description 任务重试策略
"""
from enum import Enum
from schedule.manageTaskStatus import ManageTaskStatus
from schedule.task import Task


class PreConditionType(Enum):
    DataDriven = "DataDriven"
    TaskDriven = "TaskDriven"
    CodeType = "PreConditionType"


class PreCondition(object):
    task = Task()

    def create(self, task):
        condition = PreCondition()
        condition.task = task
        return condition

    def is_true(self):
        if self.task.pre_condition_type == PreConditionType.DataDriven:
            return self.check_data_driven()
        else:
            return self.check_task_driven()

    def check_data_driven(self):
        mts = ManageTaskStatus()
        return mts.detect_task_src(self.task.task_id, self.task.current_execute_date_id)

    def check_task_driven(self):
        mts = ManageTaskStatus()
        return mts.detect_pre_task(self.task.task_id, self.task.current_execute_date_id)
