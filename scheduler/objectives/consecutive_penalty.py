from .base_objective import BaseObjective


class Consecutive0900PenaltyObjective(BaseObjective):
    """
    같은 사람이 같은 주에 '0900' 근무가 연속해서 배정되는 것을 최소화하는 목적 함수
    -   연속된 날짜에 '0900' 근무가 배정되는 경우 패널티를 부여하여,
        동일인에게 아침 근무가 몰리는 현상을 완화한다.
    -   예: A직원이 월요일 0900, 화요일 0900 근무 시 → penalty 1 발생.
    """

    def build(self):
        penalties = []

        if "0900" not in self.config.start_times:
            return 0

        s0 = self.config.start_times.index("0900")

        for p in range(self.config.num_persons):
            for w in range(self.config.num_weeks):
                for d in range(self.config.num_days - 1):
                    both = self.model.NewIntVar(
                        0, 1, f"cons0900_{self.config.persons[p]}_w{w}_d{d}"
                    )
                    self.model.AddBoolAnd(
                        [
                            self.s_model.start_shift[(p, w, d, s0)],
                            self.s_model.start_shift[(p, w, d + 1, s0)],
                        ]
                    ).OnlyEnforceIf(both)
                    self.model.AddBoolOr(
                        [
                            self.s_model.start_shift[(p, w, d, s0)].Not(),
                            self.s_model.start_shift[(p, w, d + 1, s0)].Not(),
                        ]
                    ).OnlyEnforceIf(both.Not())
                    penalties.append(both)

        return sum(penalties)
