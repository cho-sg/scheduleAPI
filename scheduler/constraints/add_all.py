"""
제약사항 정의
"""

from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel
from itertools import product
from scheduler.constraints.week_day_constraint import WeekdayConstraintBuilder
from scheduler.constraints.weekend_constraint import WeekendConstraint
from scheduler.constraints.custom_off_constraint import CustomOffConstraint
from scheduler.constraints.friday_saturday_constraint import FridaySaturdayConstraint
from scheduler.constraints.no_sole_constraint import NoSoloConstraint
from scheduler.constraints.saturday_constraint import SaturdayConstraint
from scheduler.constraints.not_allow_constraint import NotAllowConstraint


def add_constraints(config: ScheduleConfig, s_model: ScheduleModel):
    """
    모든 제약 조건 추가
    """
    WeekdayConstraintBuilder(config, s_model).add()
    WeekendConstraint(config, s_model).add()
    CustomOffConstraint(config, s_model).add()
    SaturdayConstraint(config, s_model).apply()
    FridaySaturdayConstraint(config, s_model).apply()
    NoSoloConstraint(config, s_model).apply()
    NotAllowConstraint(config, s_model).apply()
