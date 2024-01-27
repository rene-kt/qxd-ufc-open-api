from fastapi import FastAPI, HTTPException, Request
from database import redis
import json
from model.api_user import ApiUser
from model.create_api_key import CreateApiKey
from model.keys import *
from datetime import datetime
from fastapi.openapi.utils import get_openapi

from config import PROFILE

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="qxd-ufc-open-api",
        version="1.0.0",
        description="Open API for University Federal of Ceará Quixadá's Campus (https://www.quixada.ufc.br/)",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
 
 
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
        
        teacher = json.loads(redis.get_by_id(TEACHER, subject["teacherId"]))
        obj = {
            "id" : subject["id"],
            "discipline": json.loads(redis.get_by_id(DISCIPLINE, subject["disciplineId"])),
            "teacher": {
                "id": teacher["id"],
                "name": teacher["name"]
            },
            
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

def handle_json_list(list):
    result = []
    for item in list:
        result.append(json.loads(item))
    return result
