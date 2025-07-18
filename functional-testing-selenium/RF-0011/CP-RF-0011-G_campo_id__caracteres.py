import sys
import os

# Hacemos que Python pueda ver la carpeta raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

input_attempt = "X" * 65  # Intentamos ingresar 65 caracteres

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Clic en '+ Add New Course'
    add_course = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add New Course')]")))
    add_course.click()
    print("✅ Paso 1: Se hizo clic en '+ Add New Course'.")

    time.sleep(1)

    # Paso 2: Llenar campos
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys(input_attempt)

    # Verificar que solo se hayan ingresado 64 caracteres
    actual_value = course_id_input.get_attribute("value")
    if len(actual_value) == 64:
        print("✅ Course ID restringido correctamente a 64 caracteres.")
    else:
        print(f"❌ Course ID aceptó {len(actual_value)} caracteres.")

    course_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']")))
    course_name_input.clear()
    course_name_input.send_keys("Curso con ID límite")

    print("✅ Paso 2: Resto de campos llenados.")

    # Paso 3: Verificar si el botón está habilitado
    add_button = wait.until(EC.presence_of_element_located((
        By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]"
    )))

    if add_button.is_enabled():
        print("✅ Botón habilitado como se esperaba.")
        add_button.click()
        print("✅ Curso enviado correctamente.")
    else:
        print("❌ El botón estaba deshabilitado, pero debería estar activo.")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-G.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-G.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
