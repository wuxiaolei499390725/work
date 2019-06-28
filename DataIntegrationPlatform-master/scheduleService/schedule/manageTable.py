"""
author wanghaiying
date 20190601
description 数据表的实体类
"""
from array import array


class ManageTable(object):
    def __init__(self, tablename=None, databaseid=None, description=None, enabled=None, last_update_time=None,
                 original_tablename=None, tablename_expression=None):
        self._tablename = tablename
        self._databaseid = databaseid
        self._description = description
        self._enabled = enabled
        self._lastupdatetime = last_update_time
        self._originaltablename = original_tablename
        self._tablenameexpression = tablename_expression

    def getTaskSrcTable(taskID):
        return array.array(ManageTable)
