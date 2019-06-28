"""
author wanghaiying
date 20190601
description 调度实体类
"""
from datetime import date
from enum import Enum

from schedule.timerThread import TimerThread


class ManageSchedule(object):
    def __init__(self, origin_date=None, date_id=None, is_trade_date=None, is_weekly_date=None, is_monthly_date=None,
                 memo=None):
        self._origin_date = origin_date
        self._date_id = date_id
        self._is_trade_date = is_trade_date
        self._is_weekly_date = is_weekly_date
        self._is_monthly_date = is_monthly_date
        self._memo = memo

    def get(self):
        res = list()
        res.append(ManageSchedule())
        return res


class Schedule:
    def __init__(self):
        self._last_load_time = date(1900, 1, 1)
        self._scheduleTable = list()
        self._scheduleTable.append(ManageSchedule())

    def is_time_to_refresh(self):
        return (date() - self._last_load_time) > TimerThread.interval

    def load_schedule_from_db(self):
        if self.scheduleTable is None or self.is_time_to_refresh():
            ms = ManageSchedule()
            ds = ms.get()
            if ds is None or 0 == len(ds):
                return
            if self.scheduleTable:
                self._scheduleTable = ds
            self._last_load_time = date()

    def create(self, type):
        if type == ScheduleType.Custom:
            return CustomSchedule()
        else:
            return Schedule

    def is_trade_day(self, dt):
        # TODO
        return True

    def min_excute_date_id(self, task):
        # TODO
        return 1

    def max_excute_date_id(self, task):
        # TODO
        return 10

    def get_excute_date_id(self, task, dt):
        # TODO
        return 5

    def get_column_by_schedule_type(self, type):
        # TODO
        return "IsWeeklyDate"

    def get_excute_date_id(self, task, dt):
        # TODO
        return "IsWeeklyDate"


class CustomSchedule(Schedule):
    def get_excute_date_id(self, task, dt):
        # TODO
        return 1


class ScheduleType(Enum):
    TradeDaily = "TradeDaily"
    Weekly = "Weekly"
    Monthly = "Monthly"
    Custom = "Custom"
    CodeType = "ScheduleType"
