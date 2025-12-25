from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel


class NotAllowConstraint:
    """
    특정 사람이 특정 시간대에 근무하지 못하도록 제약을 추가
    ex) not_allow_persons = [["0900", "김"], ["0900", "도"]]
    """

    def __init__(self, config, s_model):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model

    def add(self):
        for time, person in self.config.not_allow_persons:
            time_idx = self.config.start_times.index(time)
            person_idx = self.config.persons.index(person)

            for w in range(self.config.num_weeks):
                for d in range(self.config.num_days):
                    self.model.Add(
                        self.s_model.start_shift[(person_idx, w, d, time_idx)] == 0
                    )
