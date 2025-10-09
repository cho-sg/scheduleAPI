"""
스케줄링 설정 클래스
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class ScheduleConfig:
    persons: List[str]
    days: List[str]  # 평일 리스트 (ex ['월','화',...])
    start_times: List[str]  # 출근 시간대 (ex ['0900','0930'...])
    week_day: List[List[int]]  # 주별 요일 필요 인원 (num_weeks x num_days)
    end_day: List[int]  # 주별 토요일 필요 인원 (length num_weeks)
    end_day_set: List[List[str]]  # 주별 권장 토요 인원 그룹 (사람 이름)
    start_times_sets: Dict[int, List[str]] = field(default_factory=dict)
    offs: List[Tuple[str, int, str]] = field(
        default_factory=list
    )  # (person, week, dayname)
    not_offs: List[Tuple[str, int, str]] = field(
        default_factory=list
    )  # (person, week, dayname)
    teams: List[List[str]] = field(default_factory=list)  # <-- 팀 필드 추가
    no_solo_persons: list[list[str]] = None  # [["1000", "도"], ...]
    not_allow_persons: list[list[str]] = None  # [["0900", "김"], ...]

    time_limit_seconds: int = 20

    @property
    def num_persons(self):
        return len(self.persons)

    @property
    def num_weeks(self):
        return len(self.week_day)

    @property
    def num_days(self):
        return len(self.days)

    @property
    def num_starts(self):
        return len(self.start_times)
