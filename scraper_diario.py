from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time
import json
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://futbolibretv.pages.dev/")
time.sleep(5)

eventos = driver.find_elements(By.CSS_SELECTOR, ".evento")
partidos_lista = []

for evento in eventos:
    try:
        nombre = evento.find_element(By.CSS_SELECTOR, ".nombre-evento").text.strip()
        
        driver.execute_script("arguments[0].scrollIntoView();", evento)
        evento.click()
        time.sleep(0.5)
        
        url_actual = driver.current_url
        url_codificada = quote(url_actual, safe=':/#?=&')
        
        partidos_lista.append({
            "partido": nombre,
            "link": url_codificada
        })
        
        driver.execute_script("arguments[0].click();", evento)
        time.sleep(0.2)
    except Exception as e:
        print("Error con un partido:", e)

driver.quit()

# Crear el código Python para bot.py
python_code = f"""PARTIDOS_JSON = {{
  "partidos": {json.dumps(partidos_lista, indent=2, ensure_ascii=False)}
}}"""

print(f"✅ Extracción completada. {len(partidos_lista)} partidos encontrados.")

# Guardar en un archivo temporal
with open("partidos_actualizados.py", "w", encoding="utf-8") as f:
    f.write(python_code)

print("📁 Archivo 'partidos_actualizados.py' creado")
