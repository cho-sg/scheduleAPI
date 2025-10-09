from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ortools.sat.python import cp_model
from run_scheduler import run

app = FastAPI()

origins = [
    "https://scheduleweb.onrender.com",
    "http://127.0.0.1:8000"
]

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,  # 쿠키/세션을 사용하는 경우 필요
    allow_origins=["*"],  # 모든 도메인 허용
    allow_methods=["*"],  # GET, POST 등 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
def read_root():
    return {"message": "OR-Tools FastAPI Server Running!"}

@app.get("/solve")
def solve_problem(limit: int = 10):
    model = cp_model.CpModel()
    x = model.NewIntVar(0, limit, "x")
    y = model.NewIntVar(0, limit, "y")
    model.Add(x + y <= limit)
    model.Maximize(x + y)
    solver = cp_model.CpSolver()
    solver.Solve(model)
    return {"x": solver.Value(x), "y": solver.Value(y)}

@app.get('/schedule')
def run_schedule():
    return run()
    return {"result":True}


