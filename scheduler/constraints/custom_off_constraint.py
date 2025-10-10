from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel
from ortools.sat.python import cp_model


class CustomOffConstraint:
    """
    휴무(offs)와 반드시 근무(not_offs) 제약을 관리하는 클래스
    """

    def __init__(self, config: ScheduleConfig, s_model: ScheduleModel):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model

    def add(self):
        """offs와 not_offs 제약 추가"""
        # offs (휴무)
        for person, week, day in self.config.offs:
            p_idx = self.config.persons.index(person)
            d_idx = self.config.days.index(day)
            self.model.Add(self.s_model.shift[(p_idx, week - 1, d_idx)] == 0)

        # not_offs (반드시 근무)
        for person, week, day in self.config.not_offs:
            p_idx = self.config.persons.index(person)
            d_idx = self.config.days.index(day)
            self.model.Add(self.s_model.shift[(p_idx, week - 1, d_idx)] == 1)
