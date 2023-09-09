from fastapi import FastAPI, HTTPException, Request
from database import redis
from database import sql
import json
from model.api_user import ApiUser
from model.create_api_key import CreateApiKey
from model.keys import *
import time
import uuid
from datetime import datetime
from send_email import send_email

app = FastAPI()


@app.middleware("http")
async def middleware(request: Request, call_next):
    now = datetime.now()
    url = request.url.path
    api_key = "api_key"
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
async def get_all_subject():
    return handle_json_list(redis.get_all(SUBJECT))


@app.get("/subject/{id}")
async def get_subject(id):
    return json.loads(redis.get_by_id(SUBJECT, id))


@app.post("/key")
async def create_api_key(payload: CreateApiKey):
    result = ApiUser(str(uuid.uuid4()), payload.name, payload.email, False)
    redis.insert(result.to_dict(), API_KEY)
    await send_email.send(payload.email, result.api_key)
    return {"key": result.api_key}


@app.get("/key/{api_key}")
async def activate_api_key(api_key: str):
    redis.activate_api_key(api_key)
    return "Chave ativada com sucesso!"


def handle_json_list(list):
    result = []
    for item in list:
        result.append(json.loads(item))
    return result
