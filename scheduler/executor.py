import importlib
from .vars import build_model
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
    vars = build_model(config)

    add_strategy(config, vars)
    add_constraints(config, vars)
    add_objective(config, vars)

    solver, status = solve(vars, config)

    return {
        "schedule": outputs.get_schedule_json(solver, config, vars, status),
        "summary": outputs.get_summary_json(solver, config, vars, status),
    }
