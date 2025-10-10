"""
목적항수 정의
"""

from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleModel


def add_weekday_imbalance(config: ScheduleConfig, vars: ScheduleModel):
    """
    평일 근무 불균형
    """
    model = vars.model
    total_weekday = [
        sum(
            vars.shift[(p, w, d)]
            for w in range(config.num_weeks)
            for d in range(config.num_days)
        )
        for p in range(config.num_persons)
    ]
    min_week = model.NewIntVar(0, config.num_weeks * config.num_days, "min_week")
    max_week = model.NewIntVar(0, config.num_weeks * config.num_days, "max_week")
    for t in total_weekday:
        model.Add(t >= min_week)
        model.Add(t <= max_week)
    return max_week - min_week


def add_weekend_imbalance(config: ScheduleConfig, vars: ScheduleModel):
    """
    주말 근무 불균형
    """
    model = vars.model
    total_weekend = [
        sum(vars.shift_end[(p, w)] for w in range(config.num_weeks))
        for p in range(config.num_persons)
    ]
    min_end = model.NewIntVar(0, config.num_weeks, "min_end")
    max_end = model.NewIntVar(0, config.num_weeks, "max_end")
    for t in total_weekend:
        model.Add(t >= min_end)
        model.Add(t <= max_end)
    return max_end - min_end


def add_time_slot_imbalance(config: ScheduleConfig, vars: ScheduleModel):
    """
    시간대별 근무 불균형
    """
    model = vars.model
    slot_imbalances = []

    for s_idx, st in enumerate(config.start_times):
        counts = []
        for p_idx in range(config.num_persons):
            count = model.NewIntVar(
                0,
                config.num_weeks * config.num_days,
                f"{config.persons[p_idx]}_{st}_count",
            )
            model.Add(
                count
                == sum(
                    vars.start_shift[(p_idx, w, d_idx, s_idx)]
                    for w in range(config.num_weeks)
                    for d_idx in range(config.num_days)
                )
            )
            counts.append(count)

        min_slot = model.NewIntVar(0, config.num_weeks * config.num_days, f"min_{st}")
        max_slot = model.NewIntVar(0, config.num_weeks * config.num_days, f"max_{st}")
        for c in counts:
            model.Add(c >= min_slot)
            model.Add(c <= max_slot)

        imbalance = model.NewIntVar(
            0, config.num_weeks * config.num_days, f"imbalance_{st}"
        )
        model.Add(imbalance == max_slot - min_slot)
        slot_imbalances.append(imbalance)

    return slot_imbalances


def add_team_penalty(config: ScheduleConfig, vars: ScheduleModel):
    """
    팀 불일치 패널티만, config.teams 사용
    """
    model = vars.model
    penalty_vars = []

    for w in range(config.num_weeks):
        for day in range(config.num_days):
            for team in config.teams:  # <-- 여기 수정
                team_vars = [
                    vars.shift[(config.persons.index(p), w, day)] for p in team
                ]

                # 모두 근무하면 1, 아니면 0
                all_working = model.NewBoolVar(
                    f"all_working_w{w}_d{day}_{'_'.join(team)}"
                )
                model.AddMinEquality(all_working, team_vars)

                # 패널티 = 1 - all_working
                penalty_var = model.NewIntVar(
                    0, 1, f"team_penalty_w{w}_d{day}_{'_'.join(team)}"
                )
                model.Add(penalty_var == 1 - all_working)

                penalty_vars.append(penalty_var)

    return penalty_vars


def add_early_count_soft(model, vars, config):
    """
    같은 주에서 사람들간의 0900 근무 횟수 차이를 최소화
    """
    diffs = []
    for w in range(config.num_weeks):
        for p1 in range(config.num_persons):
            for p2 in range(p1 + 1, config.num_persons):
                diff = model.NewIntVar(
                    0, config.num_days, f"early_diff_w{w}_p{p1}_p{p2}"
                )
                model.Add(diff >= vars.early_count[(p1, w)] - vars.early_count[(p2, w)])
                model.Add(diff >= vars.early_count[(p2, w)] - vars.early_count[(p1, w)])
                diffs.append(diff)
    return diffs


def add_0900_consecutive_penalty(config: ScheduleConfig, vars: ScheduleModel):
    """
    같은 주에서 연속된 요일에 0900 근무가 나오면 penalty
    """
    model = vars.model
    penalties = []

    if "0900" not in config.start_times:
        return penalties

    s0 = config.start_times.index("0900")

    for p in range(config.num_persons):
        for w in range(config.num_weeks):
            for d in range(config.num_days - 1):
                both = model.NewIntVar(0, 1, f"cons0900_{config.persons[p]}_w{w}_d{d}")
                model.AddBoolAnd(
                    [
                        vars.start_shift[(p, w, d, s0)],
                        vars.start_shift[(p, w, d + 1, s0)],
                    ]
                ).OnlyEnforceIf(both)
                model.AddBoolOr(
                    [
                        vars.start_shift[(p, w, d, s0)].Not(),
                        vars.start_shift[(p, w, d + 1, s0)].Not(),
                    ]
                ).OnlyEnforceIf(both.Not())
                penalties.append(both)

    return penalties


def add_objective(config: ScheduleConfig, vars: ScheduleModel):
    """
    목적함수 추가
    """
    model = vars.model

    weekday_imbalance = add_weekday_imbalance(config, vars)
    # weekend_imbalance = add_weekend_imbalance(config, vars)
    slot_imbalances = add_time_slot_imbalance(config, vars)
    team_penalties = add_team_penalty(config, vars)
    early_diffs = add_early_count_soft(model, vars, config)
    cons0900_penalties = add_0900_consecutive_penalty(config, vars)

    # 목적식: 필요시 가중치 조절 가능
    imbalance = (
        weekday_imbalance * 1
        # + weekend_imbalance * 1
        + sum(slot_imbalances) * 1
        + sum(team_penalties) * 1
        + sum(early_diffs) * 1
        + sum(cons0900_penalties) * 1
    )
    model.Minimize(imbalance)
