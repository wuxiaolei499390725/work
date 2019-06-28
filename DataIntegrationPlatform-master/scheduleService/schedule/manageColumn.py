"""
author wanghaiying
date 20190601
description 数据列的实体类
"""
from array import array


class ManageColumn(object):
    def __init__(self, tableid=None, column_name=None, data_type=None, data_type_name=None, length=None, precision=None,
                 scale=None, nullable=None, index=None, description=None):
        self._tableid = tableid
        self._column_name = column_name
        self._data_type = data_type
        self._data_type_name = data_type_name
        self._length = length
        self._precision = precision
        self._scale = scale
        self._nullable = nullable
        self._index = index
        self._description = description

    def getTaskSrcColumn(taskID):
        return array.array(ManageColumn)


if __name__ == '__main__':
    col = ManageColumn(tableid=1)
    print(col._tableid)
