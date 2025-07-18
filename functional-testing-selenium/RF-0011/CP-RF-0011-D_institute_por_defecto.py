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

    # Paso 2: Verificar zona horaria preseleccionada
    try:
        label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Time Zone')]")))
        container = label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiFormControl-root')]")
        timezone_button = container.find_element(By.XPATH, ".//div[@role='button']")
        selected_timezone = timezone_button.text.strip()

        if "UTC" in selected_timezone or "Lima" in selected_timezone:
            print("✅ Zona horaria preseleccionada correctamente con:", selected_timezone)
        else:
            print(f"❌ Zona horaria inválida o no preseleccionada: {selected_timezone}")
    except Exception as e:
        print("❌ No se pudo verificar la zona horaria:", e)

    # Paso 3: Llenar los campos restantes
    course_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseId']")))
    course_id_input.clear()
    course_id_input.send_keys("CS109")

    course_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='courseName']")))
    course_name_input.clear()
    course_name_input.send_keys("Programación de Sistemas")
    print("✅ Paso 2: Campos 'Course ID' y 'Name' llenados.")

    # Paso 4: Presionar botón 'Add Course'
    register_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(text(),'Add Course')] | //button[contains(text(),'Register Course')]"
    )))
    register_button.click()
    print("✅ Paso 3: Botón 'Add Course' presionado.")

    time.sleep(2)

    # Validación final: curso agregado a la lista
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "CS109" in body_text and "Programación de Sistemas" in body_text:
        print("🎉 Curso creado exitosamente y aparece en la lista. ✅")
    else:
        print("❌ El curso no aparece en la lista.")

    # Captura de evidencia
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0011-E.png")
    print("📸 Captura guardada: screenshots/IMG-1-CP-RF-0011-E.png")

except Exception as e:
    print("❌ Error durante la ejecución:", e)

time.sleep(3)
driver.quit()
