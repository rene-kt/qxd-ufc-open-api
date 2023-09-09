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
from model.teacher import Teacher

def execute(flag = False):
    if(flag == False): return
    opts = webdriver.FirefoxOptions()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
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

            teacher["disciplines"] = list(codes)  # Converta o conjunto para uma lista
            saved = Teacher(str(uuid.uuid4()), teacher["name"], teacher["disciplines"])
            redis.insert_teacher(saved)

            # Volte para a página inicial
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            saved = Teacher(str(uuid.uuid4()), teacher["name"], teacher["disciplines"])
            redis.insert_teacher(saved)
            print(f"Erro ao processar {teacher['name']}: {str(e)}")
        finally: 
            total += 1
    driver.quit()

                

