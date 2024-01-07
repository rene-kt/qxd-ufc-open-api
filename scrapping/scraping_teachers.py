from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import uuid
from database import redis
from model.keys import TEACHER
from model.teacher import Teacher
from scrapping.try_connection import try_connection

def build_id(name: str):
    words = name.split(" ")
    initials = []
    for word in words:
        if word in ["de", "da", "do", "dos", "das", "e", "a"]: continue
        initials.append(word[0])
        initials.append(word[1])
    return "".join(initials).upper()

def execute(flag = False):
    if(flag == False): return
    
    driver = try_connection()
    print("Connection successfull established")
    regex = r'QXD\d+'

    driver.get("https://www.quixada.ufc.br/docente/")
    conteudo = driver.find_element(By.ID, "conteudo")
    rows = conteudo.find_elements(By.CLASS_NAME, "row")
    total = 1
    for row in rows:
        print(f'Processing {total} of {len(rows)}')
        div = row.find_element(By.CLASS_NAME, "col-md-10")
        name = div.find_element(By.TAG_NAME, "h2")  
        teacher = {
            "name": name.text,
            "disciplines": []
        }
        link = div.find_element(By.TAG_NAME, "a")
        link_url = link.get_attribute("href")

        # Abre a página do professor
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link_url)

        try:
            sigaa = driver.find_elements(By.XPATH, "//a[contains(text(),'si3.ufc.br')]")
            if(sigaa): sigaa[0].click()
            else: 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            driver.find_element(By.CLASS_NAME, "disciplinas_ministradas").click()
            table = driver.find_element(By.CLASS_NAME, "listagem")
            disciplines = table.find_elements(By.XPATH, "//a[starts-with(text(),'QXD')]")

            codes = set()
            for td in disciplines:
                resultados = re.findall(regex, td.text)
                if resultados:
                    id = resultados[0]
                    codes.add(id)

            teacher["disciplines"] = list(codes)
            saved = Teacher(build_id(teacher["name"]), teacher["name"], teacher["disciplines"])
            redis.insert_teacher(saved)

            # Volte para a página inicial
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            saved = Teacher(build_id(teacher["name"]), teacher["name"], teacher["disciplines"])
            redis.insert_teacher(saved)
            print(f"Erro ao processar {teacher['name']}: {str(e)}")
        finally: 
            total += 1
    
