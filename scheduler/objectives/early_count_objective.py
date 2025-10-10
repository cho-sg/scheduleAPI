from .base_objective import BaseObjective


class EarlyCountObjective(BaseObjective):
    """
    같은 주에서 사람들 간의 0900 근무 횟수 차이를 최소화
    """

    def build(self):
        diffs = []
        for w in range(self.config.num_weeks):
            for p1 in range(self.config.num_persons):
                for p2 in range(p1 + 1, self.config.num_persons):
                    diff = self.model.NewIntVar(
                        0, self.config.num_days, f"early_diff_w{w}_p{p1}_p{p2}"
                    )
                    self.model.Add(
                        diff
                        >= self.s_model.early_count[(p1, w)]
                        - self.s_model.early_count[(p2, w)]
                    )
                    self.model.Add(
                        diff
                        >= self.s_model.early_count[(p2, w)]
                        - self.s_model.early_count[(p1, w)]
                    )
                    diffs.append(diff)

        return sum(diffs)
