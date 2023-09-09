import redis
from .discipline import Discipline
from .teacher import Teacher
from .subject import Subject
import json
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def delete(): 
    r.flushall()

def insert_teacher(teacher: Teacher):
    key = f'teacher:{teacher.id}'
    value = json.dumps(teacher.to_dict())
    print(f'Insert teacher ${value}')
    r.sadd("teacher", value)
    r.set(key, value)
    
    for discipline in teacher.disciplines:
        if(get_disciplines_by_code(discipline) != None):
            subject = Subject(str(uuid.uuid4()), teacher.id, discipline)
            insert_subject(subject)
        
def get_teachers():
    return r.smembers('teacher')

def get_teachers_by_id(id: str): 
    key = f'teacher:{id}'
    return r.get(key)

def insert_discipline(discipline: Discipline):
    key = f'discipline:{discipline.code}'
    value = json.dumps(discipline.to_dict())
    print(f'Insert discipline ${value}')
    r.sadd("discipline", value)
    r.set(key, value)
    
def get_disciplines():
    return r.smembers('discipline')

def get_disciplines_by_code(code: str):
    key = f'discipline:{code}'
    return r.get(key)

def insert_subject(subject: Subject):
    key = f'subject:{subject.id}'
    value = json.dumps(subject.to_dict())
    print(f'Insert subject ${value}')
    r.sadd("subject", value)
    r.set(key, value)
    
def get_subjects():
    return r.smembers('subject')

def get_subjects_by_id(id: str):
    key = f'subject:{id}'
    return r.get(key)
