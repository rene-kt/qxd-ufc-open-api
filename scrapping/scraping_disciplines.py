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

def extract_pre_requisite(element):
    if element.text != "–":
        try:
            return element.find_element(By.TAG_NAME, "a").text
        except Exception:
            pass
    return None

def execute(flag = False): 
    if(flag == False): return
    opts = webdriver.FirefoxOptions()
    opts.headless = False
    driver = webdriver.Firefox(options=opts)
    driver.get("https://cc.quixada.ufc.br/estrutura-curricular/estrutura-curricular/")
    rows = driver.find_elements(By.TAG_NAME, "tr")
    total = 1
    filtered_rows = list(filter(lambda row: row.get_attribute("id").startswith(("QX", "PRG")), rows))
    for row in filtered_rows:
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

    driver.close()