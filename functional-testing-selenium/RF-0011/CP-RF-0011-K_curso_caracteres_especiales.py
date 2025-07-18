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

    # Paso 2: Llenar campos (incluye caracteres especiales en Course Name)
    course_id_input = wait.until(EC.presence_of_element_located((By.NAME, "courseId")))
    course_id_input.clear()
    course_id_input.send_keys("CS303")

    course_name_input = wait.until(EC.presence_of_element_located((By.NAME, "courseName")))
    course_name_input.clear()
    course_name_input.send_keys("Curso @ Avanzado!")
    print("✅ Paso 2: Campos llenados correctamente (con caracteres especiales en el nombre).")

    # Paso 3: Presionar botón Add
    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")))
    register_button.click()
    print("✅ Paso 3: Botón 'Add Course' presionado.")

    # Esperar brevemente para ver si hay mensaje de error
    time.sleep(2)

    # Verificar si aparece el curso en la lista (caso exitoso)
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Curso @ Avanzado!" in body_text:
        print("🎉 Curso creado exitosamente con caracteres especiales en el nombre. ✅")
    else:
        print("❌ No se detectó el curso creado. Puede que haya un error.")

    # Guardar captura
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-K.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0011-K.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
