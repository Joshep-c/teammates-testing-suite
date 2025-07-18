import sys
import os

# Hacemos que Python pueda ver la carpeta raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Clic en '+ Add New Course'
    add_course = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add New Course')]")))
    add_course.click()
    print("✅ Paso 1: Se hizo clic en '+ Add New Course'.")

    time.sleep(1)

    # Paso 2: No llenar campos (dejamos todo vacío)

    # Paso 3: Verificar si el botón está deshabilitado
    try:
        add_button = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]"
        )))
        if not add_button.is_enabled():
            print("✅ Botón 'Add Course' está deshabilitado como se esperaba (todos los campos vacíos).")
        else:
            print("❌ Botón 'Add Course' está habilitado, pero debería estar deshabilitado.")
    except Exception as e:
        print("❌ No se pudo verificar el estado del botón:", e)

    # Captura para evidencia
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-F.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-F.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
