"""
스케줄링 문제 풀이
"""

from ortools.sat.python import cp_model
from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleVars
from typing import Tuple


def solve(vars: ScheduleVars, config: ScheduleConfig) -> Tuple[cp_model.CpSolver, int]:
    """
    스케줄링 문제 풀이
    """
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = config.time_limit_seconds
    status = solver.Solve(vars.model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("해를 찾을 수 없습니다.")

    return solver, status
