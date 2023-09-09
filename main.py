from database import redis, sql
from model.keys import DISCIPLINE, TEACHER
from scrapping import scraping_teachers, scraping_disciplines
import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()

HOSTNAME = os.getenv("API_HOST")
PORT = os.getenv("API_PORT")
PROFILE = os.getenv("APP_PROFILE")


if __name__ == "__main__":
    print(f'Starting application on host: {HOSTNAME}, with port {PORT} on profile {PROFILE}')        
    sql.init()
    uvicorn.run("controllers.api:app", host="0.0.0.0", port=int(PORT))
    if redis.get_all(DISCIPLINE) == set():
        scraping_disciplines.execute(True)
    if redis.get_all(TEACHER) == set():
        scraping_teachers.execute(True)
