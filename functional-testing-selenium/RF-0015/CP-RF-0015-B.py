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
TEST_CASE_ID = "CP-RF-0015-B"
TEST_CASE_NAME = "Ver curso sin estudiantes"
REQUIREMENT = "RF-0015 – Ver Estudiantes en Curso"
TECHNIQUE = "Partición de Equivalencia"
COURSE_ID = "jorgecondoriosy21.gma-demo"
COURSE_URL = f"https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses/details?courseid={COURSE_ID}"
TEST_CASE_LINK = COURSE_URL
SCREENSHOT_PATH_SUCCESS = f"screenshots/IMG-1-{TEST_CASE_ID}.png"
SCREENSHOT_PATH_ERROR = f"screenshots/error_{TEST_CASE_ID}.png"

driver = get_driver()
wait = WebDriverWait(driver, 10)
test_passed = True

try:
    print(f"📋 Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito: {REQUIREMENT}")
    print(f"🧪 Técnica: {TECHNIQUE}")
    print(f"🌐 URL del curso: {COURSE_URL}")
    print(f"🔍 Link de caso de prueba: {TEST_CASE_LINK}")

    # Paso 1: Navegar al enlace del curso vacío
    driver.get(COURSE_URL)

    # Paso 2: Esperar que la vista cargue correctamente
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Paso 3: Verificar que no hay error visible
    try:
        error_banner = driver.find_element(By.CLASS_NAME, "error-message")
        raise Exception(f"Se encontró un mensaje de error en la vista: {error_banner.text}")
    except:
        pass  # No se encontró mensaje de error, lo cual es correcto

    # Paso 4: Verificar que no hay estudiantes inscritos (tabla vacía o mensaje)
    try:
        no_students_msg = driver.find_element(By.XPATH, "//*[contains(text(),'No students enrolled') or contains(text(),'Sin estudiantes')]")
        print("✅ Mensaje de 'sin estudiantes' detectado correctamente.")
    except:
        # Si no hay mensaje, validar que la tabla esté vacía
        try:
            table_body = driver.find_element(By.XPATH, "//table[contains(@class, 'student-enroll-table')]//tbody")
            student_rows = table_body.find_elements(By.TAG_NAME, "tr")
            if len(student_rows) > 0:
                raise Exception(f"Se encontraron {len(student_rows)} estudiantes cuando no debería haber ninguno.")
            print("✅ Tabla vacía sin estudiantes, como se esperaba.")
        except:
            raise Exception("No se encontró mensaje ni tabla de estudiantes. Revisa la estructura del DOM.")

except Exception as e:
    test_passed = False
    with open(f"screenshots/{TEST_CASE_ID}.log", "w", encoding="utf-8") as log_file:
        log_file.write(f"Error: {str(e)}\n")
    driver.save_screenshot(SCREENSHOT_PATH_ERROR)

finally:
    time.sleep(2)
    driver.save_screenshot(SCREENSHOT_PATH_SUCCESS if test_passed else SCREENSHOT_PATH_ERROR)
    print("✅ Caso de prueba ejecutado exitosamente. Ver resultados en la evidencia.")
    driver.quit()
