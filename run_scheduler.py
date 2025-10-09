import importlib
from scheduler.vars import build_vars
from scheduler.strategy import add_strategy
from scheduler.constraints.add_all import add_constraints
from scheduler.objective import add_objective
from scheduler.solver import solve
from scheduler import outputs
from typing import Dict, Any

def run() -> Dict[str, Any]:
    config_module = importlib.import_module("scheduler.config.m10_p5")
    config = config_module.config

    vars = build_vars(config)

    add_strategy(config, vars)
    add_constraints(config, vars)
    add_objective(config, vars)

    solver, status = solve(vars, config)

    return {
        "schedule" : outputs.get_schedule_detailed_json(solver, config, vars, status),
        "summary": outputs.get_summary_json(solver, config, vars, status)
    }

    # outputs.print_schedule_console_detailed(solver, config, vars, status)
    # outputs.print_summary(solver, config, vars, status)
    # outputs.save_schedule_excel_time_vertical("schedule_m10_p5.xlsx", solver, config, vars)

# vars.debug_print(solver)
