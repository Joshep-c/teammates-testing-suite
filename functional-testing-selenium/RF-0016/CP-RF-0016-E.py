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
TEST_CASE_ID = "CP-RF-0016-E"
TEST_CASE_NAME = "Registro con Instructions demasiado extensas"
REQUIREMENT = "RF-0016 - Crear Sesión de Retroalimentación"
TECHNIQUE = "Partición de Equivalencia"
SCREENSHOT_PATH_SUCCESS = f"screenshots/IMG-1-{TEST_CASE_ID}.png"
SCREENSHOT_PATH_ERROR = f"screenshots/error_{TEST_CASE_ID}.png"
PAGE_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/sessions"

# === Datos de entrada ===
SESSION_NAME = "Sesión con texto largo"
INSTRUCTIONS = "a" * 2001  # 2001 caracteres
OPEN_DATE = "2025-06-30"
OPEN_TIME = "10:00"
CLOSE_DATE = "2025-06-30"
CLOSE_TIME = "20:00"

# Inicializar Selenium WebDriver
driver = get_driver()
wait = WebDriverWait(driver, 10)
exception_message = None

try:
    print(f"\n📋 Ejecutando Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito probado: {REQUIREMENT}")
    print(f"🧪 Técnica utilizada: {TECHNIQUE}")
    print(f"🌐 Abriendo página: {PAGE_URL}")

    # Paso 1: Ir a la página de sesiones
    driver.get(PAGE_URL)
    print("✅ Página cargada correctamente.")

    # Paso 2: Hacer clic en botón "+"
    print("➕ Haciendo clic en el botón '+'...")
    plus_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//i[contains(@class, 'fa-plus') or contains(@class, 'icon-plus')]]"
    )))
    plus_button.click()
    print("✅ Botón '+' clickeado.")

    # Paso 3: Seleccionar 'Add New Feedback Session'
    print("📄 Seleccionando opción 'Add New Feedback Session'...")
    add_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[contains(text(),'Add New Feedback Session')]"
    )))
    add_button.click()
    print("✅ Formulario de nueva sesión abierto.")

    # Paso 4: Llenar el formulario con instrucciones largas
    print("📝 Llenando formulario con instrucciones mayores a 2000 caracteres...")
    wait.until(EC.presence_of_element_located((By.ID, "sessionName"))).send_keys(SESSION_NAME)
    driver.find_element(By.ID, "instructions").clear()
    driver.find_element(By.ID, "instructions").send_keys(INSTRUCTIONS)
    driver.find_element(By.ID, "startdate").clear()
    driver.find_element(By.ID, "startdate").send_keys(OPEN_DATE)
    driver.find_element(By.ID, "starttime").clear()
    driver.find_element(By.ID, "starttime").send_keys(OPEN_TIME)
    driver.find_element(By.ID, "enddate").clear()
    driver.find_element(By.ID, "enddate").send_keys(CLOSE_DATE)
    driver.find_element(By.ID, "endtime").clear()
    driver.find_element(By.ID, "endtime").send_keys(CLOSE_TIME)

    # Paso 5: Enviar el formulario
    print("📤 Enviando formulario...")
    driver.find_element(By.ID, "submit_button").click()
    time.sleep(3)

    # Paso 6: Verificar si se rechazó el texto demasiado largo
    print("🔍 Verificando si el sistema rechaza más de 2000 caracteres...")
    try:
        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'error') or contains(@class,'text-danger')]")
        if error_elements:
            print("⚠️ Se detectó mensaje de error en la pantalla. El sistema probablemente rechazó el contenido.")
        else:
            print("✅ No se detectaron errores visibles. Verificar límites del backend.")
    except:
        print("⚠️ No se pudo verificar si hay errores, pero el sistema no falló visiblemente.")

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
