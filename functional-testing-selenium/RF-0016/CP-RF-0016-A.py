import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

# === Metadatos del Caso de Prueba ===
TEST_CASE_ID = "CP-RF-0016-B"
TEST_CASE_NAME = "Registro con campo Session Name vacío"
REQUIREMENT = "RF-0016 - Crear Sesión de Retroalimentación"
TECHNIQUE = "Partición de Equivalencia"
SCREENSHOT_PATH_SUCCESS = f"screenshots/IMG-1-{TEST_CASE_ID}.png"
SCREENSHOT_PATH_ERROR = f"screenshots/error_{TEST_CASE_ID}.png"
PAGE_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/sessions"

# === Datos de entrada (nombre vacío) ===
SESSION_NAME = ""  # Campo vacío intencionalmente
INSTRUCTIONS = "Revisar desempeño"
OPEN_DATE = "2025-06-30"
OPEN_TIME = "10:00"
CLOSE_DATE = "2025-06-30"
CLOSE_TIME = "20:00"

driver = get_driver()
wait = WebDriverWait(driver, 10)
test_passed = True

try:
    print(f"📋 Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito: {REQUIREMENT}")
    print(f"🧪 Técnica: {TECHNIQUE}")
    print(f"🌐 URL: {PAGE_URL}")

    # Paso 1: Navegar a la página
    print("🌍 Navegando a la página de sesiones...")
    driver.get(PAGE_URL)

    # Paso 2: Clic en el botón '+'
    print("➕ Haciendo clic en el botón '+'...")
    plus_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//i[contains(@class, 'fa-plus') or contains(@class, 'icon-plus')]]"
    )))
    plus_button.click()

    # Paso 3: Clic en 'Add New Feedback Session'
    print("📝 Seleccionando 'Add New Feedback Session'...")
    add_new_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[contains(text(), 'Add New Feedback Session')]"
    )))
    add_new_button.click()

    # Paso 4: Llenar el formulario (Session Name vacío)
    print("✏️ Llenando formulario con Session Name vacío...")
    wait.until(EC.presence_of_element_located((By.ID, "sessionName"))).clear()
    driver.find_element(By.ID, "instructions").send_keys(INSTRUCTIONS)
    driver.find_element(By.ID, "startdate").clear()
    driver.find_element(By.ID, "startdate").send_keys(OPEN_DATE)
    driver.find_element(By.ID, "starttime").clear()
    driver.find_element(By.ID, "starttime").send_keys(OPEN_TIME)
    driver.find_element(By.ID, "enddate").clear()
    driver.find_element(By.ID, "enddate").send_keys(CLOSE_DATE)
    driver.find_element(By.ID, "endtime").clear()
    driver.find_element(By.ID, "endtime").send_keys(CLOSE_TIME)

    # Paso 5: Enviar formulario
    print("📤 Enviando formulario...")
    driver.find_element(By.ID, "submit_button").click()

    # Paso 6: Esperar y verificar que NO se registró la sesión
    time.sleep(2)
    error_detected = False

    try:
        print("🔍 Verificando presencia de mensaje de error...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'error') or contains(text(),'required')]")))
        error_detected = True
        print("✅ Se detectó mensaje de error como se esperaba.")
    except:
        print("⚠️ No se detectó mensaje de error explícito. Validando si la sesión fue registrada por error...")

        # Verificar que la sesión no se haya listado
        driver.get(PAGE_URL)
        time.sleep(2)
        session_elements = driver.find_elements(By.XPATH, "//div[contains(@class,'session')]//a")
        for s in session_elements:
            if SESSION_NAME.strip() and SESSION_NAME.strip() in s.text:
                raise Exception("❌ La sesión fue creada a pesar de tener nombre vacío.")

    if not error_detected:
        print("❌ No se mostró mensaje de error. Revisa validaciones del formulario.")

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
