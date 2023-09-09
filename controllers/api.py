from fastapi import FastAPI, HTTPException, Request
from database import redis
from database import sql
import json
from model.api_user import ApiUser
from model.create_api_key import CreateApiKey
from model.keys import Keys
import time
import uuid
from datetime import datetime

app = FastAPI()


@app.middleware("http")
async def middleware(request: Request, call_next):
    now = datetime.now()
    url = request.url.path
    api_key = "api_key"
    response = await call_next(request)
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    sql.insert(api_key, now, url, str(response.status_code))
    return response

@app.get("/disciplines")
async def get_all_disciplines():
    return handle_json_list(redis.get_all(Keys.DISCIPLINE.value))


@app.get("/disciplines/{id}")
async def get_discipline(id):
    return json.loads(redis.get_by_id(Keys.DISCIPLINE.value, id))


@app.get("/teacher")
async def get_all_teacher():
    return handle_json_list(redis.get_all(Keys.TEACHER.value))


@app.get("/teacher/{id}")
async def get_teacher(id):
    return json.loads(redis.get_by_id(Keys.TEACHER.value, id))


@app.get("/subject")
async def get_all_subject():
    return handle_json_list(redis.get_all(Keys.SUBJECT.value))


@app.get("/subject/{id}")
async def get_subject(id):
    return json.loads(redis.get_by_id(Keys.SUBJECT.value, id))


@app.post("/key")
async def create_api_key(payload: CreateApiKey):
    result = ApiUser(uuid.uuid4(), payload.name, payload.email, False)
    redis.insert(Keys.API_KEY.value, result)
    return result.api_key


def handle_json_list(list):
    result = []
    for item in list:
        result.append(json.loads(item))
    return result

def is_api_key_valid(api_key: str):
    return redis.get_by_id(Keys.API_KEY.value, api_key) != None
