"""
author wanghaiying
date 20190601
description taskstatus实体类
"""
from schedule.mysql import MysqlUtil
from schedule.task import Task


def get_local_task(local_ip):
    result = list()
    sql = '''select a.*, b.priority from vw_taskwithstatus a
            left outer join tasktype b
            on a.tasktype = b.tasktype
            where enabled=1 and etlserverip = '%s'
            order by priority desc''' % local_ip
    print(sql)
    try:
        results = MysqlUtil().select(sql)
        for res in results:
            result.append(Task(task_id=res[0], task_name=res[2], task_type=res[4], execution_type=res[3], schedule_type=res[5], execution_expression=res[8]))
            # result.append(Task(task_id=res['taskid'], task_name=res['taskname'], task_type=res['tasktype'], schedule_type=res['scheduletype']))
    except Exception as e:
        print(e)
    finally:
        return result


class ManageTaskStatus:
    def __init__(self, task_id=None, last_execute_date_id=None, last_succeeded_execute_date_id=None, error_count=None,
                 error_info=None, start_time=None, complete_time=None, status=None):
        self.task_id = task_id
        self._last_execute_date_id = last_execute_date_id
        self._last_succeeded_execute_date_id = last_succeeded_execute_date_id
        self._error_count = error_count
        self._error_info = error_info
        self._start_time = start_time
        self._complete_time = complete_time
        self._status = status

    @staticmethod
    def clear_task_status():
        sql = "update taskstatus set status='Failed' where status = 'Running'"
        try:
            print(sql + ' ' + str(MysqlUtil().update(sql)))
        except Exception as e:
            print(e)

    def detect_task_src(self, task_id, current_execute_date_id):
        return True

    def detect_pre_task(self, task_id, current_execute_date_id):
        return True

    def update_task_status(self, task_id, current_execute_date_id):
        return True

if __name__ == '__main__':
    # mts = ManageTaskStatus()
    # ip = '10.35.36.45'
    ip = '127.0.0.1'
    task_list = get_local_task(ip)
    print(task_list)
