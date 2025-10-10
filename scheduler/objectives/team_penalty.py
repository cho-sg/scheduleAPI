from .base_objective import BaseObjective


class TeamPenaltyObjective(BaseObjective):
    """
    팀 불일치 패널티
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
