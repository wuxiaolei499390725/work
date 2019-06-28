from schedule.manageColumn import ManageColumn
from schedule.manageTable import ManageTable
from schedule.task import Task, TaskType


class MetadataValidator(object):
    _task = Task

    def __init__(self, task=None):
        self._task = task

    srcTable = list()
    srcTable.append(ManageTable)

    srcColumn = ManageColumn()

    @property
    def error_info(self):
        return self._error_info

    def need_validate(self):
        if self._task.TaskType == TaskType.DSA:
            return True
        return False

    def validate(self):
        # TODO
        return True

    def compare_table_metadata(self, manage_table):
        return True
