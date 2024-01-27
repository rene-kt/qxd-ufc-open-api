from fastapi import FastAPI, HTTPException, Request
from database import redis
import json
from model.api_user import ApiUser
from model.create_api_key import CreateApiKey
from model.keys import *
from datetime import datetime

from config import PROFILE

app = FastAPI()

 
@app.middleware("http")
async def middleware(request: Request, call_next):
    now = datetime.now()
    url = request.url.path
    response = await call_next(request)
    return response


@app.get("/disciplines")
async def get_all_disciplines():
    return handle_json_list(redis.get_all(DISCIPLINE))


@app.get("/disciplines/{id}")
async def get_discipline(id):
    return json.loads(redis.get_by_id(DISCIPLINE, id))


@app.get("/teacher")
async def get_all_teacher():
    return handle_json_list(redis.get_all(TEACHER))


@app.get("/teacher/{id}")
async def get_teacher(id):
    return json.loads(redis.get_by_id(TEACHER, id))


@app.get("/subject")
async def get_all_subject_detailed():
    subjects = handle_json_list(redis.get_all(SUBJECT))
    result = []
    for subject in subjects:
        obj = {
            "discipline": json.loads(redis.get_by_id(DISCIPLINE, subject["disciplineId"])),
            "teacher": json.loads(redis.get_by_id(TEACHER, subject["teacherId"])),
            "id" : subject["id"]
        }
        result.append(obj)
    return result
    
@app.get("/subject/{id}")
async def get_subject(id):
    result = json.loads(redis.get_by_id(SUBJECT, id))

    return {
        "discipline": json.loads(redis.get_by_id(DISCIPLINE, result["disciplineId"])),
        "teacher": json.loads(redis.get_by_id(TEACHER, result["teacherId"])),
        "id" : result["id"]
    }

@app.get("/courses/{id}")
async def get_courses_disciplines(id):
    return handle_json_list(redis.get_all(COURSE, id))

def handle_json_list(list):
    result = []
    for item in list:
        result.append(json.loads(item))
    return result
