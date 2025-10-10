from typing import Dict, Any
from .schedule_model import build_model
from .strategy import add_strategy
from .constraints.add_all import add_constraints
from .objectives.objective_builder import add_objective
from .solver import solve
from .config.schedule_config import ScheduleConfig
from . import outputs


def execute(config: ScheduleConfig) -> Dict[str, Any]:
    s_model = build_model(config)

    add_strategy(config, s_model)
    add_constraints(config, s_model)
    add_objective(config, s_model)

    solver, status = solve(s_model, config)

    return {
        "schedule": outputs.get_schedule_json(solver, config, s_model, status),
        "summary": outputs.get_summary_json(solver, config, s_model, status),
    }
