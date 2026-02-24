from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from datetime import datetime
import csv

#=============================================================================================

import time
import csv
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

# --- FUNCIÓN 1: EXTRAER DATOS ---
def extraer_datos_financieros(driver, ticker):
    print(f"Buscando información de: {ticker}...")
    
    # 1. Búsqueda segura (Usando ENTER en lugar de clic para que no falle con divisas)
    barra_buscar = driver.find_element(By.ID, "ybar-sbq")
    barra_buscar.clear() 
    barra_buscar.send_keys(ticker)
    time.sleep(1) # Pequeña pausa para que Yahoo despliegue opciones
    barra_buscar.send_keys(Keys.ENTER)

    time.sleep(4)
    
    # 2. Captura del precio principal (con un selector universal)
    selector_precio = '[data-testid="qsp-price"], .livePrice span'
    elemento_precio = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, selector_precio))
    )
    
    # 3. Preparamos el Diccionario con los datos fijos básicos
    datos_extraidos = {
        'Fecha_Captura': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Ticker': ticker,
        'Precio_Actual': elemento_precio.text
    }
    
    # 4. Captura de la tabla (Tu código original, pero guardando en el diccionario)
    campos_datos = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="label yf-6myrf1"]'))
    )
    campos_ressultado = driver.find_elements(By.CSS_SELECTOR, 'span[class="value yf-6myrf1"]')
    
    for indice, campo in enumerate(campos_datos):
        if indice < len(campos_ressultado):
            nombre_columna = campo.text
            valor_columna = campos_ressultado[indice].text
            # Añadimos cada fila de la tabla como una columna nueva en nuestro diccionario
            datos_extraidos[nombre_columna] = valor_columna
            
    return datos_extraidos


# --- FUNCIÓN 2: GUARDAR POR CATEGORÍA ---
def guardar_en_csv(categoria, datos_diccionario):
    # Esto creará archivos como "datos_criptos.csv" o "datos_acciones.csv" automáticamente
    nombre_archivo = f'datos_{categoria.lower()}.csv'
    
    # Comprobamos si el archivo ya existe
    archivo_existe = os.path.isfile(nombre_archivo)
    
    # Extraemos los nombres de las columnas directamente del diccionario que encontró Selenium
    # Así, si las Criptos tienen 15 datos y las Acciones 8, se adapta solo.
    columnas = list(datos_diccionario.keys())
    
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        
        # Si es la primera vez que se crea ESTE archivo, le ponemos la cabecera
        if not archivo_existe:
            escritor.writeheader()
            
        # Guardamos la fila de datos
        escritor.writerow(datos_diccionario)


#========================================================================================================

s = Service(executable_path=r"C:\Users\serre\Downloads\edgedriver_win64\msedgedriver.exe.exe")
driver = webdriver.Edge(service=s)

driver.get("https://es.finance.yahoo.com")

driver.maximize_window()

try:
    botton_aceptar = WebDriverWait(driver,10).until(
            ec.element_to_be_clickable((By.NAME, 'agree'))
    )
    botton_aceptar.click()
    time.sleep(2.5)
    print('Coockies enconttrados y aceptados')
except Exception:
    print('No se encontraron Coockies')
    pass

# --- CONFIGURACIÓN DE TU CARTERA ---
# Aquí separas claramente qué es cada cosa
cartera = {
    "Criptos": ['BTC-USD', 'ETH-USD'],
    "Acciones": ['AAPL', 'TSLA'],
    "Divisas": ['EURUSD=X']
}

# --- EJECUCIÓN PRINCIPAL ---
try:
    for categoria, lista_activos in cartera.items():
        print(f"\n===== INICIANDO CATEGORÍA: {categoria.upper()} =====")
        
        for activo in lista_activos:
            try:
                # 1. Extraemos los datos de Yahoo Finance
                diccionario_resultados = extraer_datos_financieros(driver, activo)
                
                # 2. Los guardamos en su CSV correspondiente
                guardar_en_csv(categoria, diccionario_resultados)
                
                print(f"✅ Guardado con éxito: {activo} en datos_{categoria.lower()}.csv")
                
                # Pausa de seguridad para no saturar a Yahoo Finance
                time.sleep(2) 
                
            except Exception as e:
                print(f"❌ Error al procesar {activo}: {e}")
                # Si falla una, el bucle 'for' sigue automáticamente con la siguiente

except Exception as e:
    print(f"Ocurrió un error crítico: {e}")

finally:
    driver.quit()





















# botton_usd = driver.find_element(By.ID,'tab-US')
# botton_usd.click()


# barra_buscar = driver.find_element(By.ID,"ybar-sbq")
# barra_buscar.send_keys('BTC-USD')

# boton_busqueda =driver.find_element(By.ID,'ybar-search').click()

# elemento_precio_btc = WebDriverWait(driver,10).until(
#     ec.visibility_of_element_located((By.CSS_SELECTOR,'[data-testid="qsp-price"]'))
# )

# precio_accion = elemento_precio_btc.text
# print(precio_accion)


# campos_datos = WebDriverWait(driver,10).until(
#     ec.visibility_of_all_elements_located((By.CSS_SELECTOR,'span[class="label yf-6myrf1"]'))
#     )
# campos_ressultado = driver.find_elements(By.CSS_SELECTOR,'span[class="value yf-6myrf1"]')

# for indice, campo in enumerate(campos_datos):
#     resultado = campos_ressultado[indice]
#     print(f'{indice}: {campo.text}: {resultado.text}')

# sleep(10)

#boton = driver.find_element(By.XPATH, "//button[./svg[@aria-label='icon']]")