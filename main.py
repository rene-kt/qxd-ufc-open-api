from database import db
from scrapping import scraping_teachers, scraping_disciplines

def main():
    print("main")

if __name__ == "__main__":
    teachers = db.get_teachers()
    if db.get_disciplines() == set():
        scraping_disciplines.execute(True)
    if db.get_teachers() == set():
        scraping_teachers.execute(True)
        
