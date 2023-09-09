from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from database.discipline import Discipline
from database import db

def execute(flag = False): 
    if(flag == False): return
    opts = webdriver.FirefoxOptions()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get("https://cc.quixada.ufc.br/estrutura-curricular/estrutura-curricular/")
    rows = driver.find_elements(By.TAG_NAME, "tr")
    def extract_pre_requisite(element):
        if element.text != "–":
            try:
                return element.find_element(By.TAG_NAME, "a").text
            except Exception:
                pass
        return None

    for row in rows:
        id = row.get_attribute("id")
        if id.startswith("QX") or id.startswith("PRG"):
            elements = row.find_elements(By.TAG_NAME, "td")
            pre_requisite = extract_pre_requisite(elements[4])

            discipline = Discipline(
                elements[0].text,
                elements[1].text,
                elements[2].text.replace("h", ""),
                pre_requisite
            )
            db.insert_discipline(discipline)
    driver.close()