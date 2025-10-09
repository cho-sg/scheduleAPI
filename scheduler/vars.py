from dataclasses import dataclass
from typing import Dict, Tuple
from ortools.sat.python import cp_model
from scheduler.config import ScheduleConfig


@dataclass
class ScheduleVars:
    model: cp_model.CpModel
    shift: Dict[Tuple[int, int, int], cp_model.IntVar]  # (p,w,d)
    start_shift: Dict[Tuple[int, int, int, int], cp_model.IntVar]  # (p,w,d,s)
    shift_end: Dict[Tuple[int, int], cp_model.IntVar]  # (p,w)
    early_count: Dict[Tuple[int, int], cp_model.IntVar] = None


def build_vars(config: ScheduleConfig) -> ScheduleVars:
    model = cp_model.CpModel()
    shift = {}  # (person, week, day)
    start_shift = {}  # (person, week, day, start_time)
    shift_end = {}  # (person, week)

    for p in range(config.num_persons):
        for w in range(config.num_weeks):
            for d in range(config.num_days):
                shift[(p, w, d)] = model.NewBoolVar(
                    f"shift_{config.persons[p]}_week{w}_{config.days[d]}"
                )
                for s in range(config.num_starts):
                    start_shift[(p, w, d, s)] = model.NewBoolVar(
                        f"start_{config.persons[p]}_week{w}_{config.days[d]}_{config.start_times[s]}"
                    )
            shift_end[(p, w)] = model.NewBoolVar(
                f"shift_{config.persons[p]}_week{w}_토"
            )

    # --- NEW: early_count (주단위 0900 횟수) ---
    early_count = {}
    s0 = config.start_times.index("0900")  # 0900은 항상 존재한다고 가정

    for p in range(config.num_persons):
        for w in range(config.num_weeks):
            early_count[(p, w)] = model.NewIntVar(
                0, config.num_days, f"early_count_{config.persons[p]}_w{w}"
            )
            # link: early_count == sum of start_shift for s0 over all days
            model.Add(
                early_count[(p, w)]
                == sum(start_shift[(p, w, d, s0)] for d in range(config.num_days))
            )

    return ScheduleVars(
        model=model,
        shift=shift,
        start_shift=start_shift,
        shift_end=shift_end,
        early_count=early_count,
    )
