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

    # Paso 2: Llenar campos
    course_id = "CS303"
    course_id_input = wait.until(EC.presence_of_element_located((By.NAME, "courseId")))
    course_id_input.clear()
    course_id_input.send_keys(course_id)

    course_name_input = wait.until(EC.presence_of_element_located((By.NAME, "courseName")))
    course_name_input.clear()
    course_name_input.send_keys("Curso @ Avanzado!")
    print("✅ Paso 2: Campos llenados correctamente con caracteres especiales en el nombre.")

    # Seleccionar Institute (por si acaso)
    try:
        institute_dropdown = driver.find_element(By.XPATH, "//div[label[contains(text(),'Course Institute')]]//div[@role='button']")
        institute_dropdown.click()
        time.sleep(1)
        option = driver.find_element(By.XPATH, "//li[contains(text(),'Universidad Nacional de San Agustín')]")
        option.click()
        print("🏫 Institute seleccionado.")
    except:
        print("⚠ Institute ya estaba seleccionado o no fue necesario.")

    # Seleccionar Time Zone
    try:
        timezone_dropdown = driver.find_element(By.XPATH, "//div[label[contains(text(),'Time Zone')]]//div[@role='button']")
        timezone_dropdown.click()
        time.sleep(1)
        option = driver.find_element(By.XPATH, "//li[contains(text(),'America/Lima')]")
        option.click()
        print("🌍 Time zone seleccionado.")
    except:
        print("⚠ Time zone ya estaba seleccionado o no fue necesario.")

    # Paso 3: Registrar curso
    register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")))
    register_button.click()
    print("✅ Paso 3: Botón de registro presionado.")

    # Verificar que aparece en la tabla
    course_in_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//table//td[contains(text(),'{course_id}')]"))
    )
    print("🎉 Curso creado exitosamente y aparece en la lista. ✅")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-K.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0011-K.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
