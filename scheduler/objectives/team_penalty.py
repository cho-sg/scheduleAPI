from .base_objective import BaseObjective


class TeamPenaltyObjective(BaseObjective):
    """
    팀 불일치 패널티 목적 함수

    🧾 목적:
        - 같은 팀 구성원이 동일한 날 모두 근무하지 않으면 패널티 부여
        - 팀 단위 근무 일관성을 유지하고, 팀원이 함께 근무하도록 유도

    ⚙️ 동작 방식:
        1. 모든 주(w), 모든 요일(day), 모든 팀(team) 순회
        2. 팀 구성원들의 shift 변수(team_vars) 수집
        3. AddMinEquality 사용:
            - 팀의 모든 구성원이 근무하면 all_working = 1
            - 하나라도 근무하지 않으면 all_working = 0
        4. penalty_var = 1 - all_working
            - 팀 불일치 시 penalty_var = 1
            - 팀 일치 시 penalty_var = 0
        5. penalty_vars 리스트에 추가하고 마지막에 합산하여 반환
    """

    def build(self):
        penalty_vars = []

        for w in range(self.config.num_weeks):
            for day in range(self.config.num_days):
                for team in self.config.teams:
                    team_vars = [
                        self.s_model.shift[(self.config.persons.index(p), w, day)]
                        for p in team
                    ]
                    all_working = self.model.NewBoolVar(
                        f"all_working_w{w}_d{day}_{'_'.join(team)}"
                    )
                    self.model.AddMinEquality(all_working, team_vars)

                    penalty_var = self.model.NewIntVar(
                        0, 1, f"team_penalty_w{w}_d{day}_{'_'.join(team)}"
                    )
                    self.model.Add(penalty_var == 1 - all_working)
                    penalty_vars.append(penalty_var)

        return sum(penalty_vars)
