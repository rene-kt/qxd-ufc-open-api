from database import redis
from model.keys import DISCIPLINE, TEACHER
from scrapping import scraping_teachers, scraping_disciplines
import uvicorn

from config import HOSTNAME, PORT, PROFILE

if __name__ == "__main__":
    print(f'Starting application on host: {HOSTNAME}, with port {PORT} on profile {PROFILE}')        

    if redis.get_all(DISCIPLINE) == set():
        scraping_disciplines.execute(True)
    if redis.get_all(TEACHER) == set():
        scraping_teachers.execute(True)
        
    print(f'Starting application on host: {HOSTNAME}, with port {PORT} on profile {PROFILE}')        
    uvicorn.run("controllers.api:app", host="0.0.0.0", port=int(PORT))

