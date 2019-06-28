"""
author wanghaiying
date 20190601
description 任务重试策略
"""
import datetime
from schedule.manageSchedule import Schedule


class IdleTime:
    # 交易空闲时间
    # 任务调度必须在“交易空闲时间”执行；对于非交易日，全天都是空闲时间
    # 例如：
    # 对于交易日，空闲时间配置如下：
    # 当天起始时间 = 18：00
    # 明天结束时间 = 8：00
    # 表示从当天18: 00
    # 到第二天8：00，是交易空闲时间，允许执行任务
    @property
    def time_after_today(self):
        return self._time_after_today

    @property
    def time_before_tomorrow(self):
        return self._time_before_tomorrow

    def is_idle_time(self, dt):
        try:
            # 非交易日，全天都是空闲时间
            if not Schedule.is_trade_day(dt):
                return True
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') > self._time_after_today or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') < self._time_before_tomorrow:
                return True
            return False
        except Exception as e:
            print(e)
        finally:
            return False
