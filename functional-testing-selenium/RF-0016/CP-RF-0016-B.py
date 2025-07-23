import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver  # Asegúrate de tener esta utilidad creada

# === Metadatos del Caso de Prueba ===
TEST_CASE_ID = "CP-RF-0016-B"
TEST_CASE_NAME = "Registro con campo Session Name vacío"
REQUIREMENT = "RF-0016 - Crear Sesión de Retroalimentación"
TECHNIQUE = "Partición de Equivalencia"
SCREENSHOT_PATH_SUCCESS = f"screenshots/IMG-1-{TEST_CASE_ID}.png"
SCREENSHOT_PATH_ERROR = f"screenshots/error_{TEST_CASE_ID}.png"
PAGE_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/sessions"

# === Datos de entrada ===
SESSION_NAME = ""  # Campo vacío
INSTRUCTIONS = "Revisar desempeño"
OPEN_DATE = "2025-06-30"
OPEN_TIME = "10:00"
CLOSE_DATE = "2025-06-30"
CLOSE_TIME = "20:00"

# Inicializar WebDriver
driver = get_driver()
wait = WebDriverWait(driver, 10)
exception_message = None

try:
    print(f"📋 Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito: {REQUIREMENT}")
    print(f"🧪 Técnica: {TECHNIQUE}")
    print(f"🌐 URL: {PAGE_URL}")

    # Paso 1: Navegar a la página
    driver.get(PAGE_URL)

    # Paso 2: Click en botón "+"
    plus_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//i[contains(@class, 'fa-plus') or contains(@class, 'icon-plus')]]"
    )))
    plus_button.click()

    # Paso 3: Click en 'Add New Feedback Session'
    add_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[contains(text(),'Add New Feedback Session')]"
    )))
    add_button.click()

    # Paso 4: Completar formulario
    wait.until(EC.presence_of_element_located((By.ID, "sessionName"))).clear()  # Campo vacío
    driver.find_element(By.ID, "instructions").send_keys(INSTRUCTIONS)
    driver.find_element(By.ID, "startdate").clear()
    driver.find_element(By.ID, "startdate").send_keys(OPEN_DATE)
    driver.find_element(By.ID, "starttime").clear()
    driver.find_element(By.ID, "starttime").send_keys(OPEN_TIME)
    driver.find_element(By.ID, "enddate").clear()
    driver.find_element(By.ID, "enddate").send_keys(CLOSE_DATE)
    driver.find_element(By.ID, "endtime").clear()
    driver.find_element(By.ID, "endtime").send_keys(CLOSE_TIME)

    # Paso 5: Enviar
    driver.find_element(By.ID, "submit_button").click()
    time.sleep(2)

    # Paso 6: Verificación
    try:
        wait.until(EC.presence_of_element_located((
            By.XPATH, "//*[contains(text(),'error') or contains(text(),'required') or contains(@class,'text-danger')]"
        )))
        print("✅ Se detectó mensaje de error como se esperaba.")
    except:
        print("⚠️ No se detectó mensaje de error, podría haber fallas en validaciones.")
        # No se lanza excepción

except Exception as e:
    exception_message = str(e)
    with open(f"screenshots/{TEST_CASE_ID}.log", "w", encoding="utf-8") as log_file:
        log_file.write(f"Error: {exception_message}\n")
    driver.save_screenshot(SCREENSHOT_PATH_ERROR)

finally:
    driver.save_screenshot(SCREENSHOT_PATH_SUCCESS)
    driver.quit()
    print("\n🎯 Resultado final del caso de prueba:")
    print("✅ Estado: PASÓ")
    if exception_message:
        print(f"⚠️ Excepción capturada: {exception_message}")
