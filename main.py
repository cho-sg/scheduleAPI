import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ortools.sat.python import cp_model
from scheduler.config.schedule_config import ScheduleConfig
from scheduler.executor import execute
from request.schedule_request import ScheduleRequest

app = FastAPI()
origins = ["https://scheduleweb.onrender.com", "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,  # 쿠키/세션을 사용하는 경우 필요
    allow_origins=["*"],  # 모든 도메인 허용
    allow_methods=["*"],  # GET, POST 등 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.get("/schedule")
def schedule_endpoint(request: ScheduleRequest = None):
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
    return execute(config)


@app.get("/")
def root_endpoint():
    return {"message": "OR-Tools FastAPI Server Running!"}


@app.get("/solve")
def solve_endpoint(limit: int = 10):
    model = cp_model.CpModel()
    x = model.NewIntVar(0, limit, "x")
    y = model.NewIntVar(0, limit, "y")
    model.Add(x + y <= limit)
    model.Maximize(x + y)
    solver = cp_model.CpSolver()
    solver.Solve(model)
    return {"x": solver.Value(x), "y": solver.Value(y)}
