# ==========================================
# 1. IMPORTACIONES (La caja de herramientas)
# ==========================================
# Herramientas nativas de Python:
import time         # Para hacer pausas (ej. time.sleep)
import csv          # Para crear y escribir en archivos .csv
import os           # Para interactuar con tu sistema (ej. ver si existe un archivo)
from datetime import datetime # Para guardar la hora exacta de la extracción

# Herramientas de Selenium (El "robot" virtual):
from selenium import webdriver
from selenium.webdriver.edge.options import Options # Para configurar el modo invisible (headless)
from selenium.webdriver.common.by import By         # Para buscar elementos (por ID, Clase, etc.)
from selenium.webdriver.support.ui import WebDriverWait # Para pausas "inteligentes"
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys     # Para simular teclas (ej. ENTER)

# Funciones secundarias (Los obreros)
from funciones_obreras import extraer_datos_financieros, guardar_en_csv
# ==========================================
# 2. FUNCIONES SECUNDARIAS (Los obreros)
# ==========================================
# def extraer_datos_financieros(driver, ticker):
#     """Entra a Yahoo Finance, busca el ticker y extrae los datos."""
#     print(f"Buscando información de: {ticker}...")
    
#     # Simulamos que un humano escribe y pulsa ENTER (más seguro que hacer clic en la lupa)
#     barra_buscar = driver.find_element(By.ID, "ybar-sbq")
#     barra_buscar.clear() 
#     barra_buscar.send_keys(ticker)
#     time.sleep(1) 
#     barra_buscar.send_keys(Keys.ENTER)

<<<<<<< HEAD
#     # Pausa "tonta" de 4 segundos. Obligatoria para dar tiempo a que cambie la URL 
#     # y evitar Race Conditions (que no se mezclen datos de Bitcoin con los de Apple).
#     time.sleep(4) 
=======
# --- FUNCIÓN 1: EXTRAER DATOS ---
def extraer_datos_financieros(driver, ticker):
    print(f"Buscando información de: {ticker}...")
>>>>>>> 54276c67f7cde94cd77c981d1faf8a310fff7edb
    
#     # Pausa "inteligente": Espera HASTA 10 seg a que aparezca el precio. Si aparece en el seg 1, avanza.
#     selector_precio = '[data-testid="qsp-price"], .livePrice span'
#     elemento_precio = WebDriverWait(driver, 10).until(
#         ec.visibility_of_element_located((By.CSS_SELECTOR, selector_precio))
#     )
    
#     # Preparamos la "caja" (diccionario) con los primeros datos
#     datos_extraidos = {
#         'Fecha_Captura': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'Ticker': ticker,
#         'Precio_Actual': elemento_precio.text
#     }
    
#     # Capturamos todas las etiquetas de la tabla (ej. "Volumen") y sus valores (ej. "1.2B")
#     campos_datos = WebDriverWait(driver, 10).until(
#         ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="label yf-6myrf1"]'))
#     )
#     campos_ressultado = driver.find_elements(By.CSS_SELECTOR, 'span[class="value yf-6myrf1"]')
    
#     # Emparejamos cada etiqueta con su valor y lo metemos en nuestro diccionario
#     for indice, campo in enumerate(campos_datos):
#         if indice < len(campos_ressultado):
#             datos_extraidos[campo.text] = campos_ressultado[indice].text
            
#     return datos_extraidos

# def guardar_en_csv(categoria, datos_diccionario):
#     """Guarda la caja de datos en un archivo .csv sin borrar lo anterior."""
#     nombre_archivo = f'datos_{categoria.lower()}.csv'
    
#     # Pregunta: "¿Existe ya este archivo en el disco duro?"
#     archivo_existe = os.path.isfile(nombre_archivo)
#     columnas = list(datos_diccionario.keys())
    
#     # mode='a' significa Append (Añadir). Escribe la nueva fila debajo de las que ya existen.
#     with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as archivo:
#         escritor = csv.DictWriter(archivo, fieldnames=columnas)
        
#         # Si es la primera vez que se crea, le ponemos los títulos de las columnas arriba del todo
#         if not archivo_existe:
#             escritor.writeheader()
        
#         # Guardamos la fila de datos
#         escritor.writerow(datos_diccionario)

# ==========================================
# 3. FUNCIÓN PRINCIPAL (El jefe de obra)
# ==========================================
def main():
    """Coordina todo el proceso, inicializa el navegador y maneja los errores."""
    print("Iniciando el Bot de Extracción Financiera...")
    
    # Le ponemos la "capa de invisibilidad" al navegador (Headless). 
    # Trabaja en segundo plano sin usar ventanas físicas ni tarjeta gráfica.
    opciones = Options()
    opciones.add_argument("--headless") 
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    
    # Inicializamos el driver (Selenium 4+ se encarga de buscarlo/instalarlo solo)
    driver = webdriver.Edge(options=opciones) 

<<<<<<< HEAD
    try:
        driver.get("https://es.finance.yahoo.com")
        driver.set_window_size(1920, 1080)

        # Manejo de Cookies: Intenta aceptarlas. Si no sale el pop-up, el 'except' evita que se cuelgue.
        try:
            botton_aceptar = WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.NAME, 'agree'))
            )
            botton_aceptar.click()
            time.sleep(2)
            print('✅ Cookies encontradas y aceptadas')
        except Exception:
            print('ℹ️ No se encontraron Cookies (o ya estaban aceptadas)')

        # Nuestra lista de tareas a extraer
        cartera = {
            "Criptos": ['BTC-USD', 'ETH-USD'],
            "Acciones": ['AAPL', 'TSLA'],
            "Divisas": ['EURUSD=X']
        }

        # Bucle de extracción: Recorre categorías y luego activos
        for categoria, lista_activos in cartera.items():
            print(f"\n===== INICIANDO CATEGORÍA: {categoria.upper()} =====")
            for activo in lista_activos:
                try: # Si falla un activo, el 'try' permite continuar con el siguiente sin parar el bot
                    diccionario_resultados = extraer_datos_financieros(driver, activo)
                    guardar_en_csv(categoria, diccionario_resultados)
                    print(f"✅ Guardado con éxito: {activo}")
                    time.sleep(2) 
                except Exception as e:
                    print(f"❌ Error al procesar {activo}: {e}")

    except Exception as e:
        print(f"Ocurrió un error crítico general: {e}")
        
    finally:
        # Esta línea es VITAL. Pase lo que pase (incluso si hay error fatal o le das a Stop),
        # cierra el proceso del navegador. Evita que la RAM de tu PC se sature de Edge fantasmas.
        driver.quit()
        print("\nNavegador cerrado. Fin del proceso.")

# ==========================================
# 4. PUNTO DE ENTRADA (El botón de encendido)
# ==========================================
# Seguro profesional: Solo ejecuta el código si le das al 'Play' directamente a este archivo.
# Si mañana importas este bot desde otro archivo de Python, no se ejecutará a lo loco.
if __name__ == "__main__":
    main()





















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
=======
finally:
    driver.quit()
>>>>>>> 54276c67f7cde94cd77c981d1faf8a310fff7edb
