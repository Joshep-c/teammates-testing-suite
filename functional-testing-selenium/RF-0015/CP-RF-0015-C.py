import sys
import os
import time
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

# === Metadatos del Caso de Prueba ===
TEST_CASE_ID = "CP-RF-0015-C"
TEST_CASE_NAME = "Descargar lista de estudiantes"
REQUIREMENT = "RF-0015 – Ver Estudiantes en Curso"
TECHNIQUE = "Tabla de Decisiones"
COURSE_ID = "CS303"
COURSE_URL = f"https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses/enroll?courseid={COURSE_ID}"
SCREENSHOT_PATH_SUCCESS = f"screenshots/IMG-1-{TEST_CASE_ID}.png"
SCREENSHOT_PATH_ERROR = f"screenshots/error_{TEST_CASE_ID}.png"

# Carpeta de descargas del sistema (ajusta si usas otra)
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

driver = get_driver()
wait = WebDriverWait(driver, 10)
test_passed = True

try:
    print(f"📋 Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito: {REQUIREMENT}")
    print(f"🧪 Técnica: {TECHNIQUE}")
    print(f"🌐 URL del curso: {COURSE_URL}")

    # Paso 1: Ir a la página del curso
    driver.get(COURSE_URL)

    # Paso 2: Esperar botón de descarga visible
    download_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Download') or contains(text(),'Descargar')]")
    ))

    # Paso 3: Guardar el archivo más reciente antes de la descarga
    before_download = max(glob.glob(os.path.join(DOWNLOAD_DIR, "*")), key=os.path.getctime)

    # Paso 4: Hacer clic en el botón de descarga
    download_button.click()

    # Paso 5: Esperar un poco para que se complete la descarga
    time.sleep(5)

    # Paso 6: Verificar si se descargó un nuevo archivo
    after_download = max(glob.glob(os.path.join(DOWNLOAD_DIR, "*")), key=os.path.getctime)
    if before_download == after_download:
        raise Exception("No se detectó ningún nuevo archivo descargado.")

    # Paso 7 (opcional): Validar contenido si es .csv o .txt
    if after_download.endswith(".csv") or after_download.endswith(".txt"):
        with open(after_download, 'r', encoding='utf-8') as f:
            content = f.read()
            if "Email" not in content:
                raise Exception("Archivo descargado no contiene encabezados esperados.")
        print("✅ Encabezados encontrados en el archivo.")

    print("✅ Archivo descargado correctamente.")

except Exception as e:
    test_passed = False
    with open(f"screenshots/{TEST_CASE_ID}.log", "w", encoding="utf-8") as log_file:
        log_file.write(f"Error: {str(e)}\n")
    driver.save_screenshot(SCREENSHOT_PATH_ERROR)

finally:
    time.sleep(2)
    driver.save_screenshot(SCREENSHOT_PATH_SUCCESS if test_passed else SCREENSHOT_PATH_ERROR)
    print("✅ Caso de prueba ejecutado exitosamente. Ver resultados en la evidencia.")
    driver.quit()
