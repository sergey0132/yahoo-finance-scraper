import time         # Para hacer pausas (ej. time.sleep)
import csv          # Para crear y escribir en archivos .csv
import os           # Para interactuar con tu sistema (ej. ver si existe un archivo)
from datetime import datetime # Para guardar la hora exacta de la extracción
from selenium.webdriver.common.by import By         # Para buscar elementos (por ID, Clase, etc.)
from selenium.webdriver.support.ui import WebDriverWait # Para pausas "inteligentes"
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys     # Para simular teclas (ej. ENTER)

# ==========================================
# 2. FUNCIONES SECUNDARIAS (Los obreros)
# ==========================================
def extraer_datos_financieros(driver, ticker):
    """Entra a Yahoo Finance, busca el ticker y extrae los datos."""
    print(f"Buscando información de: {ticker}...")
    
    # Simulamos que un humano escribe y pulsa ENTER (más seguro que hacer clic en la lupa)
    barra_buscar = driver.find_element(By.ID, "ybar-sbq")
    barra_buscar.clear() 
    barra_buscar.send_keys(ticker)
    time.sleep(1) 
    barra_buscar.send_keys(Keys.ENTER)

    # Pausa "tonta" de 4 segundos. Obligatoria para dar tiempo a que cambie la URL 
    # y evitar Race Conditions (que no se mezclen datos de Bitcoin con los de Apple).
    time.sleep(4) 
    
    # Pausa "inteligente": Espera HASTA 10 seg a que aparezca el precio. Si aparece en el seg 1, avanza.
    selector_precio = '[data-testid="qsp-price"], .livePrice span'
    elemento_precio = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, selector_precio))
    )
    
    # Preparamos la "caja" (diccionario) con los primeros datos
    datos_extraidos = {
        'Fecha_Captura': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Ticker': ticker,
        'Precio_Actual': elemento_precio.text
    }
    
    # Capturamos todas las etiquetas de la tabla (ej. "Volumen") y sus valores (ej. "1.2B")
    campos_datos = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="label yf-6myrf1"]'))
    )
    campos_ressultado = driver.find_elements(By.CSS_SELECTOR, 'span[class="value yf-6myrf1"]')
    
    # Emparejamos cada etiqueta con su valor y lo metemos en nuestro diccionario
    for indice, campo in enumerate(campos_datos):
        if indice < len(campos_ressultado):
            datos_extraidos[campo.text] = campos_ressultado[indice].text
            
    return datos_extraidos

def guardar_en_csv(categoria, datos_diccionario):
    """Guarda la caja de datos en un archivo .csv sin borrar lo anterior."""
    nombre_archivo = f'datos_{categoria.lower()}.csv'
    
    # Pregunta: "¿Existe ya este archivo en el disco duro?"
    archivo_existe = os.path.isfile(nombre_archivo)
    columnas = list(datos_diccionario.keys())
    
    # mode='a' significa Append (Añadir). Escribe la nueva fila debajo de las que ya existen.
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        
        # Si es la primera vez que se crea, le ponemos los títulos de las columnas arriba del todo
        if not archivo_existe:
            escritor.writeheader()
        
        # Guardamos la fila de datos
        escritor.writerow(datos_diccionario)