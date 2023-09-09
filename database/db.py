import redis

from database.keys import Keys
from .discipline import Discipline
from .teacher import Teacher
from .subject import Subject
import json
import uuid

r = redis.Redis(host='localhost', port=6379)

def delete(): 
    r.flushall()

def insert_teacher(teacher: Teacher):
    insert(teacher.to_dict(), Keys.TEACHER.value)
    
    for discipline in teacher.disciplines:
        if(get_by_id("discipline", discipline) != None):
            subject = Subject(str(uuid.uuid4()), teacher.id, discipline)
            insert(subject.to_dict(), Keys.SUBJECT.value)
        
def get_all(key: str):
    return r.smembers(key)

def get_by_id(key: str, id: str):
    return r.get(f'{key}:{id}')

def insert(obj: dict, key: str):
    value = json.dumps(obj)
    print(f'Inserting entity {value}')
    r.sadd(key, value)
    r.set(f'{key}:{obj["id"]}', value)
    
