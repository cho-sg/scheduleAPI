from abc import ABC, abstractmethod
from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel


class BaseObjective(ABC):
    """모든 목적함수 클래스의 공통 인터페이스"""

    def __init__(self, config: ScheduleConfig, s_model: ScheduleModel):
        self.config = config
        self.model = s_model.model
        self.s_model = s_model

    @abstractmethod
    def build(self):
        """목적함수 항목을 반환"""
        pass
