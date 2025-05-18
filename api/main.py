from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load student data from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "students.json")
with open(json_path) as f:
    students_data = json.load(f)

@app.get("/api")
async def get_marks(name: List[str] = Query(None)):
    """
    Get marks for one or more students by name.
    Example: /api?name=John&name=Alice
    """
    if not name:
        return {"error": "Please provide at least one name"}

    marks = []
    for student_name in name:
        mark = next((student["marks"] for student in students_data 
                     if student["name"].lower() == student_name.lower()), None)
        marks.append(mark)

    return {"marks": marks}

@app.get("/")
async def root():
    return {"message": "Naami's student Marks API. Use /api?name=John to query marks."}

