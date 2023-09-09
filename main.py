from database import redis
from database.subject import Subject
from scrapping import scraping_teachers, scraping_disciplines

def main():
    print("main")

if __name__ == "__main__":
    if redis.get_all("disciplines") == set():
        scraping_disciplines.execute(True)
    if redis.get_all("teachers") == set():
        scraping_teachers.execute(True)
        