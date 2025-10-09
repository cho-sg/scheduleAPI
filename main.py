from fastapi import FastAPI
from ortools.sat.python import cp_model
from run_scheduler import run

app = FastAPI()

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
    run()
    return {"result":True}


