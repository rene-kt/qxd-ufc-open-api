from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from database import redis
from model.discipline import Discipline
from model.keys import DISCIPLINE
from model.courses_enum import Courses
from retrying import retry
from scrapping.try_connection import try_connection
from scrapping.scraping_teachers import execute as execute_teachers

def extract_pre_requisite(element):
    if element.text != "–":
        try:
            return element.find_element(By.TAG_NAME, "a").text
        except Exception:
            pass
    return None

    
def execute(flag = False): 
    if(not flag): return
    driver = try_connection()
    print("Connection successfull established")
    driver.get("https://cc.quixada.ufc.br/estrutura-curricular/estrutura-curricular/")
    rows = driver.find_elements(By.TAG_NAME, "tr")
    total = 1
    filtered_rows = list(filter(lambda row: row.get_attribute("id").startswith(("QXD")), rows))
    print("Rows filtered")

    for row in filtered_rows:
        try:
            print(f'Processing discipline {total} of {len(filtered_rows)}')
            elements = row.find_elements(By.TAG_NAME, "td")
            pre_requisite = extract_pre_requisite(elements[4])

            discipline = Discipline(
                elements[0].text,
                elements[1].text,
                elements[2].text.replace("h", ""),
                pre_requisite,
                [Courses.CC.name]
            )
            redis.insert_discipline(discipline)
            total += 1
        except Exception as e:
            print(f"Erro ao disciplina {discipline['name']}: {str(e)}")
            
    driver.close()