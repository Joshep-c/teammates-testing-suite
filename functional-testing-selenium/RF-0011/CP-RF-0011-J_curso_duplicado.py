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

    # Paso 2: Ingresar datos con ID duplicado
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys("CS202")  # Este ID ya está registrado

    course_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']")))
    course_name_input.clear()
    course_name_input.send_keys("Curso Duplicado")

    print("✅ Paso 2: Campos llenados con ID duplicado.")

    # Paso 3: Presionar botón 'Add Course'
    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")))
    register_button.click()
    print("✅ Paso 3: Botón 'Add Course' presionado.")

    time.sleep(2)

    # Paso 4: Buscar mensajes de error visibles en pantalla
    try:
        error_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[contains(text(),'ya existente') or contains(text(),'existente') or contains(text(),'ya existe') or contains(text(),'existe')]")
        ))
        
        found = False
        for e in error_elements:
            msg = e.text.strip()
            if msg:
                print("✅ Mensaje de error detectado:", msg)
                found = True
                break
        
        if not found:
            print("❌ No se detectó mensaje de error visible en texto.")
    except Exception as e:
        print("❌ No se detectó mensaje de error (excepción):", e)

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-J.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-J.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
