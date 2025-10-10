from itertools import product
from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleModel


class WeekdayConstraintBuilder:
    def __init__(self, config: ScheduleConfig, vars: ScheduleModel):
        self.config = config
        self.vars = vars
        self.model = vars.model

    def add(self):
        """평일 요일별 필요 인원 및 시간대 제약 추가"""
        for w, d in product(range(self.config.num_weeks), range(self.config.num_days)):
            self._add_daily_constraints(w, d)

    def _add_daily_constraints(self, w: int, d: int):
        need = self.config.week_day[w][d]

        if need > 0:
            self._add_shift_sum_constraint(w, d, need)
            self._add_time_set_constraints(w, d, need)
            self._add_single_time_per_person_constraint(w, d)
        else:
            self._add_no_shift_constraint(w, d)

    def _add_shift_sum_constraint(self, w: int, d: int, need: int):
        shift_sum = sum(
            self.vars.shift[(p, w, d)] for p in range(self.config.num_persons)
        )
        self.model.Add(shift_sum == need)

    def _add_time_set_constraints(self, w: int, d: int, need: int):
        if need not in self.config.start_times_sets:
            return

        times_today = self.config.start_times_sets[need]
        for s, st in enumerate(self.config.start_times):
            required = times_today.count(st)
            self.model.Add(
                sum(
                    self.vars.start_shift[(p, w, d, s)]
                    for p in range(self.config.num_persons)
                )
                == required
            )

    def _add_single_time_per_person_constraint(self, w: int, d: int):
        for p in range(self.config.num_persons):
            self.model.Add(
                sum(
                    self.vars.start_shift[(p, w, d, s)]
                    for s in range(self.config.num_starts)
                )
                == self.vars.shift[(p, w, d)]
            )

    def _add_no_shift_constraint(self, w: int, d: int):
        for p in range(self.config.num_persons):
            self.model.Add(self.vars.shift[(p, w, d)] == 0)
            for s in range(self.config.num_starts):
                self.model.Add(self.vars.start_shift[(p, w, d, s)] == 0)
