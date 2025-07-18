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
    # Paso 1: Click en '+ Add New Course'
    add_course = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add New Course')]")))
    add_course.click()
    print("✅ Paso 1: Se hizo clic en '+ Add New Course'.")

    time.sleep(1)

    # Paso 2: Ingresar valores (nombre largo)
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys("CS200")

    course_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']")))
    course_name_input.clear()
    
    # Nombre con más de 80 caracteres
    nombre_largo = "Curso de Pruebas Automatizadas con Selenium para Validar Campos de Texto Extra Largo!!!"
    course_name_input.send_keys(nombre_largo)

    actual_text = course_name_input.get_attribute("value")
    print(f"📏 Texto ingresado en 'Course Name': {len(actual_text)} caracteres.")

    if len(actual_text) > 80:
        print("❌ El campo permite ingresar más de 80 caracteres.")
    else:
        print("✅ El campo limita correctamente a 80 caracteres.")

    # Paso 3: Click en botón 'Add Course'
    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")))
    register_button.click()
    print("✅ Paso 3: Botón 'Add Course' presionado.")

    time.sleep(2)

    # Verificar si el curso aparece
    try:
        table = driver.find_element(By.TAG_NAME, "table")
        if "CS200" in table.text:
            print("❌ El curso con nombre largo se agregó, lo cual es un error.")
        else:
            print("✅ Curso no aparece en la lista, validación correcta.")
    except:
        print("⚠ No se pudo verificar si el curso fue agregado.")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-H.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-H.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
