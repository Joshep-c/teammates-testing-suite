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

    # Paso 2: Ingresar Course ID válido
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys("CS105")
    print("✅ Paso 2: Course ID ingresado.")

    # Paso 3: No escribir el Course Name (lo dejamos vacío)

    # Paso 4: Completar los demás campos

    # Institute
    try:
        institute_dropdown = driver.find_element(By.XPATH, "//div[label[contains(text(),'Course Institute')]]//div[@role='button']")
        institute_dropdown.click()
        time.sleep(1)
        option = driver.find_element(By.XPATH, "//li[contains(text(),'Universidad Nacional de San Agustín')]")
        option.click()
        print("🏫 Institute seleccionado.")
    except:
        print("⚠ Institute ya estaba seleccionado o no fue necesario.")

    # Time Zone
    try:
        timezone_dropdown = driver.find_element(By.XPATH, "//div[label[contains(text(),'Time Zone')]]//div[@role='button']")
        timezone_dropdown.click()
        time.sleep(1)
        option = driver.find_element(By.XPATH, "//li[contains(text(),'America/Lima')]")
        option.click()
        print("🌍 Time Zone seleccionado.")
    except:
        print("⚠ Time Zone ya estaba seleccionado o no fue necesario.")

    # Verificar si el botón 'Add Course' está deshabilitado
    time.sleep(1)
    register_button = driver.find_element(By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]")
    is_disabled = register_button.get_attribute("disabled")

    if is_disabled:
        print("✅ El botón 'Add Course' está deshabilitado como se espera cuando 'Course Name' está vacío.")
    else:
        print("❌ El botón 'Add Course' está habilitado incorrectamente.")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-C.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
