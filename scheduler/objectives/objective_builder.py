from .weekday_imbalance import WeekdayImbalanceObjective
from .time_slot_imbalance import TimeSlotImbalanceObjective
from .team_penalty import TeamPenaltyObjective
from .consecutive_penalty import Consecutive0900PenaltyObjective
from .early_count_soft_objective import EarlyCountSoftObjective

# 필요한 경우 weekend_imbalance 등도 import


class ObjectiveBuilder:
    def __init__(self, config, s_model):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model
        self.objectives = []

    def add(self, objective_class, weight=1):
        self.objectives.append((objective_class(self.config, self.s_model), weight))

    def build(self):
        total_expr = 0
        for obj, weight in self.objectives:
            total_expr += weight * obj.build()
        self.model.Minimize(total_expr)


def add_objective(config, s_model):
    builder = ObjectiveBuilder(config, s_model)
    builder.add(WeekdayImbalanceObjective, weight=1)
    builder.add(TimeSlotImbalanceObjective, weight=1)
    builder.add(TeamPenaltyObjective, weight=1)
    builder.add(Consecutive0900PenaltyObjective, weight=1)
    builder.add(EarlyCountSoftObjective, weight=1)
    builder.build()
