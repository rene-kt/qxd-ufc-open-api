from database import redis, sql
from model.keys import DISCIPLINE, TEACHER
from scrapping import scraping_teachers, scraping_disciplines
import uvicorn

if __name__ == "__main__":
    if redis.get_all(DISCIPLINE) == set():
        scraping_disciplines.execute(True)
    if redis.get_all(TEACHER) == set():
        scraping_teachers.execute(True)
        
    sql.init()
    uvicorn.run("controllers.api:app", host="0.0.0.0", port=8080)
        