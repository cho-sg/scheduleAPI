from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel
from ortools.sat.python import cp_model


class WeekendConstraint:
    """
    주말(토요일, 일요일) 근무 제약 관리 클래스
    """

    def __init__(self, config: ScheduleConfig, s_model: ScheduleModel):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model

    def add(self):
        """제약 추가"""
        for w in range(self.config.num_weeks):
            self.model.Add(
                sum(
                    self.s_model.shift_end[(p, w)]
                    for p in range(self.config.num_persons)
                )
                == self.config.end_day[w]
            )
