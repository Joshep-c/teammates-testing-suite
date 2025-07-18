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

    # Paso 2: Llenar campos con ID inválido
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys("CS@101!")

    course_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']")))
    course_name_input.clear()
    course_name_input.send_keys("Curso con caracteres inválidos")

    print("✅ Paso 2: Campos llenados con Course ID inválido.")

    # Paso 3: Click en botón 'Add Course'
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")))
    add_button.click()
    print("✅ Paso 3: Botón 'Add Course' presionado.")

    time.sleep(2)

    # Verificar si aparece algún mensaje de error (adaptar si hay validación visible)
    error_found = False
    try:
        # Ejemplo genérico de búsqueda de mensaje de error
        error = driver.find_element(By.XPATH, "//*[contains(text(), 'inválido') or contains(text(), 'Inválido')]")
        print(f"✅ Error visible detectado: {error.text}")
        error_found = True
    except:
        print("⚠ No se detectó mensaje de error visible.")

    # Verificar si curso NO se agregó (intentamos buscarlo en la lista)
    try:
        table = driver.find_element(By.TAG_NAME, "table")
        if "CS@101!" in table.text:
            print("❌ El curso con ID inválido se agregó, lo cual es un error.")
        else:
            print("✅ Curso no aparece en la lista, validación correcta.")
    except:
        print("⚠ No se pudo verificar si el curso se agregó.")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-I.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-I.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
