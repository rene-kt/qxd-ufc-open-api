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

opts = webdriver.FirefoxOptions()
opts.headless = False
driver = webdriver.Firefox(options=opts)
regex = r'QXD\d+'
teachers = []

driver.get("https://www.quixada.ufc.br/docente/")
conteudo = driver.find_element(By.ID, "conteudo")
rows = conteudo.find_elements(By.CLASS_NAME, "row")

for row in rows:
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
        teachers.append(teacher)

        # Volte para a página inicial
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        teachers.append(teacher)
        print(f"Erro ao processar {teacher['name']}: {str(e)}")

print(teachers)
driver.quit()

            

