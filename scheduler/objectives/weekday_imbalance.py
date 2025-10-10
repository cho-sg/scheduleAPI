from .base_objective import BaseObjective


class WeekdayImbalanceObjective(BaseObjective):
    """
    평일 근무 불균형 최소화
    """

    def build(self):
        total_weekday = [
            sum(
                self.s_model.shift[(p, w, d)]
                for w in range(self.config.num_weeks)
                for d in range(self.config.num_days)
            )
            for p in range(self.config.num_persons)
        ]
        min_week = self.model.NewIntVar(
            0, self.config.num_weeks * self.config.num_days, "min_week"
        )
        max_week = self.model.NewIntVar(
            0, self.config.num_weeks * self.config.num_days, "max_week"
        )
        for t in total_weekday:
            self.model.Add(t >= min_week)
            self.model.Add(t <= max_week)
        return max_week - min_week
