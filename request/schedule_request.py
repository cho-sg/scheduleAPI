from pydantic import BaseModel
from typing import List, Dict


class ScheduleRequest(BaseModel):
    persons: List[str]
    week_day: List[str]
    end_day: str
    end_day_set: List[str]
    offs: List[str]
    not_offs: List[str]
    teams: List[str]
    no_solo_persons: List[str]
    not_allow_persons: List[str]
