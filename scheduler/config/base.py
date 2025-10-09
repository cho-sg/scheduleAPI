"""
스케줄링 설정 정의
"""

from .core import ScheduleConfig

days = ["월", "화", "수", "목", "금"]
start_times = ["0900", "0900_S", "0930", "1000"]
start_times_sets = {
    2: ["0900", "0900"],
    3: ["0900", "0930", "1000"],
    4: ["0900", "0930", "1000", "1000"],
    5: ["0900", "0900_S", "0930", "1000", "1000"],
}


def build_config(
    persons,
    week_day,
    end_day,
    end_day_set,
    offs,
    not_offs,
    teams,
    no_solo_persons,
    not_allow_persons,
):
    """
    ScheduleConfig 객체 생성
    """
    return ScheduleConfig(
        days=days,
        start_times=start_times,
        start_times_sets=start_times_sets,
        persons=persons,
        week_day=week_day,
        end_day=end_day,
        end_day_set=end_day_set,
        offs=offs,
        not_offs=not_offs,
        teams=teams,
        no_solo_persons=no_solo_persons,
        not_allow_persons=not_allow_persons,
        time_limit_seconds=20,
    )


def validate_config(config):
    # 1) end_day_set 크기 검사
    for w in range(config.num_weeks):
        if config.end_day[w] > len(config.end_day_set[w]):
            raise ValueError(
                f"Week {w+1}: end_day ({config.end_day[w]}) > len(end_day_set) ({len(config.end_day_set[w])}). "
                "허용 그룹이 부족합니다."
            )

    # 2) start_times_sets 존재 검사: week_day에서 필요 수가 매핑되는 경우 start_times_sets 정의 여부
    for w in range(config.num_weeks):
        for d in range(config.num_days):
            need = config.week_day[w][d]
            if need > 0 and need not in config.start_times_sets:
                raise ValueError(
                    f"Week {w+1} day {config.days[d]}: need={need}, but start_times_sets does not define key {need}."
                )

    # 3) required start time counts 합이 need와 일치하는지(안정성 검사)
    #    (이건 선택적 체크 — start_times_sets[need]의 길이가 need와 다르면 의도 확인)
    for k, arr in config.start_times_sets.items():
        if len(arr) != k:
            # 경고로 처리하거나 예외로 처리 가능
            print(
                f"Warning: start_times_sets[{k}] length {len(arr)} != needed {k}. (이는 의도된 것일 수 있습니다)"
            )

    # 4) start_times에 "0900"/"1000" 존재 확인 (옵션)
    if "0900" not in config.start_times:
        print("Warning: '0900' not in start_times; early_count 관련 제약은 무시됩니다.")
    if "1000" not in config.start_times:
        print("Warning: '1000' not in start_times; 금요일-1000 관련 제약은 무시됩니다.")
