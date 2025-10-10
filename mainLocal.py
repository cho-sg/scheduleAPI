from scheduler.executor import execute
from scheduler import outputs

result = execute()
outputs.print_schedule_json(result["schedule"])
outputs.print_summary_json(result["summary"])
