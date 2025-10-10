from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel


class SaturdayConstraint:
    """
    토요일 근무자는 반드시 권장 그룹(end_day_set)에 속해야 함
    """

    def __init__(self, config: ScheduleConfig, s_model: ScheduleModel):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model

    def apply(self):
        for w in range(self.config.num_weeks):
            allowed = [self.config.persons.index(p) for p in self.config.end_day_set[w]]
            for p in range(self.config.num_persons):
                if p not in allowed:
                    # 강제: 토요일 근무 불가
                    self.model.Add(self.s_model.shift_end[(p, w)] == 0)
