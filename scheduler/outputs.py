"""
출력
"""

from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleVars
from ortools.sat.python import cp_model
from tabulate import tabulate
from openpyxl import Workbook
from typing import Dict, Any

def get_summary_json(
    solver: cp_model.CpSolver, config: ScheduleConfig, vars: ScheduleVars, status
) -> Dict[str, Any]:
    """
    요약 통계를 JSON 형태로 반환
    """
    per_person_weekday = {p: 0 for p in config.persons}
    per_person_weekend = {p: 0 for p in config.persons}
    per_person_by_day = {p: {d: 0 for d in config.days} for p in config.persons}
    per_person_by_time = {p: {st: 0 for st in config.start_times} for p in config.persons}

    total_by_day = {d: 0 for d in config.days}
    total_by_time = {st: 0 for st in config.start_times}
    total_weekend = 0

    for w in range(config.num_weeks):
        for d_idx, d in enumerate(config.days):
            for p_idx, p in enumerate(config.persons):
                worked = False
                for s_idx, st in enumerate(config.start_times):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        worked = True
                        per_person_by_time[p][st] += 1
                        break
                if worked:
                    per_person_weekday[p] += 1
                    per_person_by_day[p][d] += 1
                    total_by_day[d] += 1
            for s_idx, st in enumerate(config.start_times):
                for p_idx in range(config.num_persons):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        total_by_time[st] += 1

    for w in range(config.num_weeks):
        for p_idx, p in enumerate(config.persons):
            if solver.Value(vars.shift_end[(p_idx, w)]):
                per_person_weekend[p] += 1
                total_weekend += 1

    return {
        "per_person": {
            p: {
                "weekday": per_person_weekday[p],
                "weekend": per_person_weekend[p],
                "by_day": per_person_by_day[p],
                "by_time": per_person_by_time[p],
            }
            for p in config.persons
        },
        "total_by_day": total_by_day,
        "total_by_time": total_by_time,
        "total_weekend": total_weekend,
    }


def get_schedule_detailed_json(
    solver: cp_model.CpSolver, config: ScheduleConfig, vars: ScheduleVars, status
) -> dict:
    """
    시간대별 상세 스케줄을 JSON으로 반환
    - weekdays: 시간대별 shifts
    - weekends: 시간대 제거, 근무자 배열만
    """
    weeks_json = []

    for w in range(config.num_weeks):
        week_data = {"days": [], "weekends": []}

        # 요일별
        for d_idx, d in enumerate(config.days):
            day_shifts = []
            for s_idx, st in enumerate(config.start_times):
                assigned = [
                    config.persons[p]
                    for p in range(config.num_persons)
                    if solver.Value(vars.start_shift[(p, w, d_idx, s_idx)])
                ]
                day_shifts.append({"time": st, "person": assigned})
            week_data["days"].append({"name": d, "shifts": day_shifts})

        # 주말
        weekend_assigned = [
            config.persons[p]
            for p in range(config.num_persons)
            if solver.Value(vars.shift_end[(p, w)])
        ]
        week_data["weekends"].append({"name": "토", "person": weekend_assigned})

        weeks_json.append(week_data)

    return {"weeks": weeks_json}


def print_schedule_console_detailed(
    solver: cp_model.CpSolver, config: ScheduleConfig, vars: ScheduleVars, status
):
    """
    콘솔에 스케줄 출력 (상세: 시간대별)
    """
    for w in range(config.num_weeks):
        print(f"\n▶ 주 {w+1}")
        print("시간\t" + "\t".join(config.days) + "\t토")
        for s_idx, st in enumerate(config.start_times):
            row = [st]
            for d_idx in range(config.num_days):
                assigned = [
                    config.persons[p]
                    for p in range(config.num_persons)
                    if solver.Value(vars.start_shift[(p, w, d_idx, s_idx)])
                ]
                row.append(",".join(assigned) if assigned else "-")
            if s_idx == 0:
                assigned_end = [
                    config.persons[p]
                    for p in range(config.num_persons)
                    if solver.Value(vars.shift_end[(p, w)])
                ]
                row.append(",".join(assigned_end) if assigned_end else "-")
            else:
                row.append("-")
            print("\t".join(row))


def print_summary(
    solver: cp_model.CpSolver, config: ScheduleConfig, vars: ScheduleVars, status
):
    """
    요약 통계 출력
    """
    per_person_weekday = {p: 0 for p in config.persons}
    per_person_weekend = {p: 0 for p in config.persons}
    per_person_by_day = {p: {d: 0 for d in config.days} for p in config.persons}
    per_person_by_time = {
        p: {st: 0 for st in config.start_times} for p in config.persons
    }

    total_by_day = {d: 0 for d in config.days}
    total_by_time = {st: 0 for st in config.start_times}
    total_weekend = 0

    for w in range(config.num_weeks):
        for d_idx, d in enumerate(config.days):
            for p_idx, p in enumerate(config.persons):
                worked = False
                for s_idx, st in enumerate(config.start_times):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        worked = True
                        per_person_by_time[p][st] += 1
                        break
                if worked:
                    per_person_weekday[p] += 1
                    per_person_by_day[p][d] += 1
                    total_by_day[d] += 1
            for s_idx, st in enumerate(config.start_times):
                for p_idx in range(config.num_persons):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        total_by_time[st] += 1

    for w in range(config.num_weeks):
        for p_idx, p in enumerate(config.persons):
            if solver.Value(vars.shift_end[(p_idx, w)]):
                per_person_weekend[p] += 1
                total_weekend += 1

    print("\n================ 인원별 통계 ================")
    headers = ["이름", "평", "토"] + config.days + config.start_times
    table = []
    for p in config.persons:
        row = [p, per_person_weekday[p], per_person_weekend[p]]
        row.extend([per_person_by_day[p][d] for d in config.days])
        row.extend([per_person_by_time[p][st] for st in config.start_times])
        table.append(row)
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            stralign="center",
            numalign="center",
        )
    )

    print("\n================ 요일별 근무수 ================")
    headers = ["요일", "근무수"]
    table = [[d, total_by_day[d]] for d in config.days]
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            stralign="center",
            numalign="center",
        )
    )

    print("\n================ 시간별 근무수 ================")
    headers = ["시간", "근무수"]
    table = [[st, total_by_time[st]] for st in config.start_times]
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            stralign="center",
            numalign="center",
        )
    )

    print("\n================ 토요 근무수 ================")
    print(f"총 토 근무수: {total_weekend}")


def save_schedule_excel_time_vertical(
    filename: str, solver: cp_model.CpSolver, config: ScheduleConfig, vars: ScheduleVars
):
    """
    Excel 파일로 스케줄 저장 (시간대별, 요일이 열)
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Schedule"

    # -------------------------
    # 1. 스케줄 (시간 x 요일)
    # -------------------------
    ws.append(["시간/요일"] + config.days + ["토"])

    for w in range(config.num_weeks):
        ws.append([f"▶ 주 {w+1}"])
        for s_idx, st in enumerate(config.start_times):
            row = [st]
            for d_idx in range(config.num_days):
                assigned = [
                    config.persons[p]
                    for p in range(config.num_persons)
                    if solver.Value(vars.start_shift[(p, w, d_idx, s_idx)])
                ]
                row.append(",".join(assigned) if assigned else "-")
            if s_idx == 0:
                assigned_end = [
                    config.persons[p]
                    for p in range(config.num_persons)
                    if solver.Value(vars.shift_end[(p, w)])
                ]
                row.append(",".join(assigned_end) if assigned_end else "-")
            else:
                row.append("-")
            ws.append(row)

    # -------------------------
    # 2. 요약 통계
    # -------------------------
    per_person_weekday = {p: 0 for p in config.persons}
    per_person_weekend = {p: 0 for p in config.persons}
    per_person_by_day = {p: {d: 0 for d in config.days} for p in config.persons}
    per_person_by_time = {
        p: {st: 0 for st in config.start_times} for p in config.persons
    }

    total_by_day = {d: 0 for d in config.days}
    total_by_time = {st: 0 for st in config.start_times}
    total_weekend = 0

    for w in range(config.num_weeks):
        for d_idx, d in enumerate(config.days):
            for p_idx, p in enumerate(config.persons):
                worked = False
                for s_idx, st in enumerate(config.start_times):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        worked = True
                        per_person_by_time[p][st] += 1
                        break
                if worked:
                    per_person_weekday[p] += 1
                    per_person_by_day[p][d] += 1
                    total_by_day[d] += 1
            for s_idx, st in enumerate(config.start_times):
                for p_idx in range(config.num_persons):
                    if solver.Value(vars.start_shift[(p_idx, w, d_idx, s_idx)]):
                        total_by_time[st] += 1

    for w in range(config.num_weeks):
        for p_idx, p in enumerate(config.persons):
            if solver.Value(vars.shift_end[(p_idx, w)]):
                per_person_weekend[p] += 1
                total_weekend += 1

    # 2-1. 인원별 통계
    ws_summary = wb.create_sheet("Summary")
    headers = ["이름", "평", "토"] + config.days + config.start_times
    ws_summary.append(headers)
    for p in config.persons:
        row = [p, per_person_weekday[p], per_person_weekend[p]]
        row.extend([per_person_by_day[p][d] for d in config.days])
        row.extend([per_person_by_time[p][st] for st in config.start_times])
        ws_summary.append(row)

    # 2-2. 요일별 근무수
    ws_summary.append([])
    ws_summary.append(["요일", "근무수"])
    for d in config.days:
        ws_summary.append([d, total_by_day[d]])

    # 2-3. 시간별 근무수
    ws_summary.append([])
    ws_summary.append(["시간", "근무수"])
    for st in config.start_times:
        ws_summary.append([st, total_by_time[st]])

    # 2-4. 토요 근무수
    ws_summary.append([])
    ws_summary.append(["총 토 근무수", total_weekend])

    wb.save(filename)
    print(f"Excel 파일 저장 완료: {filename}")
