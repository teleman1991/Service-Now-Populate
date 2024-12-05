from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import json
from pathlib import Path
from pydantic import BaseModel

app = FastAPI(title='Computer Problems API')

class Problem(BaseModel):
    problem: str
    solution: str
    category: str

def load_problems() -> List[Problem]:
    data_file = Path('data/computer_problems.json')
    if not data_file.exists():
        return []
    with open(data_file, 'r', encoding='utf-8') as f:
        return [Problem(**p) for p in json.load(f)]

@app.get('/problems/', response_model=List[Problem])
async def get_problems(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    problems = load_problems()
    
    if category:
        problems = [p for p in problems if p.category.lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        problems = [
            p for p in problems
            if search_lower in p.problem.lower() or search_lower in p.solution.lower()
        ]
    
    return problems

@app.get('/problems/{problem_id}', response_model=Problem)
async def get_problem(problem_id: int):
    problems = load_problems()
    if 0 <= problem_id < len(problems):
        return problems[problem_id]
    raise HTTPException(status_code=404, detail='Problem not found')

@app.get('/categories/')
async def get_categories():
    problems = load_problems()
    return list(set(p.category for p in problems))