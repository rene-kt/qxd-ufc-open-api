from fastapi import FastAPI
import uvicorn
from database import redis
import json

from database.keys import Keys 
app = FastAPI()

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

def handle_json_list(list):
    result = []
    for item in list:
        result.append(json.loads(item))
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

