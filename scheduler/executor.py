import importlib
from .schedule_model import build_model
from .strategy import add_strategy
from .constraints.add_all import add_constraints
from .objective import add_objective
from .solver import solve
from .config.base import build_config
from . import outputs
from typing import Dict, Any


def execute() -> Dict[str, Any]:
    config_module = importlib.import_module("scheduler.config.m10_p5")
    config = build_config(
        config_module.persons,
        config_module.week_day,
        config_module.end_day,
        config_module.end_day_set,
        config_module.offs,
        config_module.not_offs,
        config_module.teams,
        config_module.no_solo_persons,
        config_module.not_allow_persons,
    )
    s_model = build_model(config)

    add_strategy(config, s_model)
    add_constraints(config, s_model)
    add_objective(config, s_model)

    solver, status = solve(s_model, config)

    return {
        "schedule": outputs.get_schedule_json(solver, config, s_model, status),
        "summary": outputs.get_summary_json(solver, config, s_model, status),
    }
