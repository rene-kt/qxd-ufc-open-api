from dotenv import load_dotenv
import redis
import json
from model.api_user import ApiUser
from model.discipline import Discipline
from model.keys import *
from model.subject import Subject
from model.teacher import Teacher

import os
load_dotenv()

PORT = os.getenv("REDIS_PORT")

r = redis.Redis(host='redis', port=6379)

def delete(): 
    r.flushall()

def insert_teacher(teacher: Teacher):
    saved = get_by_id(TEACHER, teacher.id)
    if saved:
        value = json.loads(saved)
        teacher.disciplines = set(value["disciplines"] + teacher.disciplines)
        
    insert(teacher.to_dict(), TEACHER)
    
    for discipline in teacher.disciplines:
        if(get_by_id(DISCIPLINE, discipline) != None):
            subject = Subject(f'{discipline}-{teacher.id}', teacher.id, discipline)
            insert(subject.to_dict(), SUBJECT)

def insert_discipline(discipline: Discipline):
    saved = get_by_id(DISCIPLINE, discipline.id)
    if saved:
        print(f"Discipline {discipline.id} already exists in the given courses {discipline.courses}")
        value = json.loads(saved)
        discipline.courses = set(value["courses"] + discipline.courses)
    
    for course in discipline.courses: insert_update_course(course, discipline)
    insert(discipline.to_dict(), DISCIPLINE)

    
def insert_update_course(course: str, discipline: Discipline):
    key = f'{COURSE}:{course}'
    print(f"Inserting discipline {discipline.id} in course {course}")
    r.sadd(key, json.dumps(discipline.to_dict()))
    
def get_all(key: str, id: str = None):
    if id: return r.smembers(f'{key}:{id}')
    return r.smembers(key)

def get_by_id(key: str, id: str):
    return r.get(f'{key}:{id}')

def insert(obj: dict, key: str):
    value = json.dumps(obj)
    print(f'Inserting entity {value}')
    r.sadd(key, value)
    r.set(f'{key}:{obj["id"]}', value)
    return value
    
def activate_api_key(api_key: str):
    api_user = get_by_id(API_KEY, api_key)
    if(api_user == None): return
    api_user = json.loads(api_user)
    api_user["active"] = True
    return insert(api_user, API_KEY)
    