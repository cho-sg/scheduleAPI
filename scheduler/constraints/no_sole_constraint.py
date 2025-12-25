from scheduler.config import ScheduleConfig
from scheduler.schedule_model import ScheduleModel


class NoSoloConstraint:
    """
    특정 사람이 특정 시간대에 혼자 근무하지 못하도록 강제
    예: no_solo_persons = [["1000", "도"], ["1000", "김"]]
    """

    def __init__(self, config: ScheduleConfig, s_model: ScheduleModel):
        self.config = config
        self.s_model = s_model
        self.model = s_model.model

    def add(self):
        for time, person in self.config.no_solo_persons:
            time_idx = self.config.start_times.index(time)
            person_idx = self.config.persons.index(person)

            for w in range(self.config.num_weeks):
                for d in range(self.config.num_days):
                    total_at_time = sum(
                        self.s_model.start_shift[(p, w, d, time_idx)]
                        for p in range(len(self.config.persons))
                    )
                    # 본인이 근무하면 최소 2명 이상 필요
                    self.model.Add(
                        total_at_time
                        >= self.s_model.start_shift[(person_idx, w, d, time_idx)] * 2
                    )
