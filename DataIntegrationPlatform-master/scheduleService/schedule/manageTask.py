
class ManageTask:
    def __init__(self, task_id=None, etl_server_ip=None, task_name=None, execution_type=None, task_type=None,
                 schedule_type=None, pre_condition_type=None, enabled=None, start_execute_date_id=None):
        self._task_id = task_id
        self._etl_server_ip = etl_server_ip
        self._task_name = task_name
        self._execution_type = execution_type
        self._task_type = task_type
        self._schedule_type = schedule_type
        self.__pre_condition_type = pre_condition_type
        self._enabled = enabled
        self._start_execute_date_id = start_execute_date_id
