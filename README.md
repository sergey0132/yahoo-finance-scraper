# 📈 Yahoo Finance Data Scraper Bot

Un bot de extracción de datos automatizado (Web Scraper) desarrollado en Python. Este script navega por Yahoo Finance, extrae información financiera en tiempo real de diferentes activos (Criptomonedas, Acciones y Divisas) y genera bases de datos limpias en formato CSV.

## 🚀 Características Principales

* **Extracción Dinámica:** Identifica automáticamente las columnas de datos de la web y genera las cabeceras de los CSV de forma dinámica.
* **Navegación Invisible (Headless):** Configurado con Selenium y WebDriver Manager para ejecutarse en segundo plano sin consumir recursos gráficos.
* **Manejo de Excepciones y Tiempos:** Incorpora pausas estratégicas (`WebDriverWait`) para evitar *Race Conditions* y bloqueos por carga dinámica del DOM (AJAX).
* **Gestión de Cookies:** Detecta y acepta automáticamente los pop-ups de normativas de datos europeos.
* **Arquitectura Modular:** Código estructurado profesionalmente con punto de entrada (`__main__`) y funciones separadas por responsabilidad.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Librerías principales:** `Selenium`, `webdriver-manager`
* **Librerías nativas:** `csv`, `os`, `time`, `datetime`

## ⚙️ Instalación y Uso

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)

pip install -r requirements.txt

python "prrueebas con selñenium.py"

# 🔮 Roadmap y Futuras Mejoras (Fase Data Science)
Este proyecto es la Fase 1 (Recolección de Datos) de un pipeline de Data Science más grande. Las próximas actualizaciones incluirán:

* [ ] Data Cleaning: Script adicional con Pandas para limpieza de datos (conversión de strings "1.2B" a floats numéricos, tratamiento de valores nulos).

* [ ] Machine Learning: Entrenamiento de un modelo predictivo (Regresión/Random Forest) usando el histórico de datos capturado por el bot.
