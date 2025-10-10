import importlib
from scheduler.config.schedule_config import ScheduleConfig
from scheduler.executor import execute
from scheduler import outputs

config_module = importlib.import_module("scheduler.config.m10_p5")
config = ScheduleConfig(
    persons=config_module.persons,
    week_day=config_module.week_day,
    end_day=config_module.end_day,
    end_day_set=config_module.end_day_set,
    offs=config_module.offs,
    not_offs=config_module.not_offs,
    teams=config_module.teams,
    no_solo_persons=config_module.no_solo_persons,
    not_allow_persons=config_module.not_allow_persons,
)

result = execute(config)
outputs.print_schedule_json(result["schedule"])
outputs.print_summary_json(result["summary"])
