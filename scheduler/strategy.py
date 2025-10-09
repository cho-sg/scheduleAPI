"""
모델 탐색 전략 지정
"""

from ortools.sat.python import cp_model
from scheduler.config import ScheduleConfig
from scheduler.vars import ScheduleVars


def add_strategy(config: ScheduleConfig, vars: ScheduleVars):
    """
    각 (week, day)에서 'persons' 순서대로 근무를 탐색하도록 모델 전략 지정
    """
    model = vars.model

    for w in range(config.num_weeks):
        for d in range(config.num_days):
            # 이 날 근무 여부 변수들을 사람 순서대로 묶기
            day_vars = [vars.shift[(p, w, d)] for p in range(config.num_persons)]

            # 순서 강제: persons 배열 순서대로 먼저 배정
            model.AddDecisionStrategy(
                day_vars,
                cp_model.CHOOSE_FIRST,  # 변수 선택: 선언 순서대로
                cp_model.SELECT_MAX_VALUE,  # 값 선택: 근무(1)를 우선
            )
