from .base_objective import BaseObjective


class TimeSlotImbalanceObjective(BaseObjective):
    """
    시간대별 근무 불균형 최소화
    """

    def build(self):
        slot_imbalances = []

        for s_idx, st in enumerate(self.config.start_times):
            counts = []
            for p_idx in range(self.config.num_persons):
                count = self.model.NewIntVar(
                    0,
                    self.config.num_weeks * self.config.num_days,
                    f"{self.config.persons[p_idx]}_{st}_count",
                )
                self.model.Add(
                    count
                    == sum(
                        self.s_model.start_shift[(p_idx, w, d_idx, s_idx)]
                        for w in range(self.config.num_weeks)
                        for d_idx in range(self.config.num_days)
                    )
                )
                counts.append(count)

            min_slot = self.model.NewIntVar(
                0, self.config.num_weeks * self.config.num_days, f"min_{st}"
            )
            max_slot = self.model.NewIntVar(
                0, self.config.num_weeks * self.config.num_days, f"max_{st}"
            )
            for c in counts:
                self.model.Add(c >= min_slot)
                self.model.Add(c <= max_slot)

            imbalance = self.model.NewIntVar(
                0, self.config.num_weeks * self.config.num_days, f"imbalance_{st}"
            )
            self.model.Add(imbalance == max_slot - min_slot)
            slot_imbalances.append(imbalance)

        return sum(slot_imbalances)
