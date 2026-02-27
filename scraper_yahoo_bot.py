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
