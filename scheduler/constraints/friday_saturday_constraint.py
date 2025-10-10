from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleModel


class FridaySaturdayConstraint:
    """
    금요일 1000 근무자는 해당 주 토요일 근무 불가
    """

    def __init__(self, config: ScheduleConfig, vars: ScheduleModel):
        self.config = config
        self.vars = vars
        self.model = vars.model

    def apply(self):
        if "금" not in self.config.days or "1000" not in self.config.start_times:
            return  # 조건이 없으면 skip

        fri_idx = self.config.days.index("금")
        time_idx = self.config.start_times.index("1000")

        for p in range(self.config.num_persons):
            for w in range(self.config.num_weeks):
                self.model.Add(
                    self.vars.shift_end[(p, w)]
                    + self.vars.start_shift[(p, w, fri_idx, time_idx)]
                    <= 1
                )
