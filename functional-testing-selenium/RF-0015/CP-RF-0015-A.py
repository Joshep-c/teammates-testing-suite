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
TEST_CASE_ID = "CP-RF-0015-A"
TEST_CASE_NAME = "Visualización completa de estudiantes inscritos"
REQUIREMENT = "RF-0015 – Ver Estudiantes en Curso"
TECHNIQUE = "Partición de Equivalencia"
COURSE_ID = "CS303"
COURSE_URL = f"https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses/enroll?courseid={COURSE_ID}"
TEST_CASE_LINK = f"https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses/details?courseid=jorgecondoriosy21.gma-demo"
SCREENSHOT_PATH_SUCCESS = "screenshots/IMG-1-CP-RF-0015-A.png"
SCREENSHOT_PATH_ERROR = "screenshots/error_CP-RF-0015-A.png"

driver = get_driver()
wait = WebDriverWait(driver, 10)
test_passed = True

try:
    print(f"📋 Caso de Prueba: {TEST_CASE_ID} - {TEST_CASE_NAME}")
    print(f"🔗 Requisito: {REQUIREMENT}")
    print(f"🧪 Técnica: {TECHNIQUE}")
    print(f"🌐 URL del curso: {COURSE_URL}")
    print(f"🔍 Link de caso de prueba: {TEST_CASE_LINK}")

    # Paso 1: Navegar al enlace del curso
    driver.get(COURSE_URL)

    # Paso 2: Esperar la tabla de estudiantes
    student_table = wait.until(EC.presence_of_element_located((
        By.XPATH, "//table[contains(@class, 'student-enroll-table')]"
    )))

    # Paso 3: Verificar encabezados
    expected_headers = ["Name", "Email", "Team"]
    headers = student_table.find_elements(By.XPATH, ".//thead//th")
    header_texts = [header.text.strip() for header in headers]
    for expected in expected_headers:
        if expected not in header_texts:
            raise Exception(f"Encabezado esperado '{expected}' no encontrado.")

    # Paso 4: Verificar que haya al menos un estudiante
    student_rows = student_table.find_elements(By.XPATH, ".//tbody/tr")
    if len(student_rows) == 0:
        raise Exception("No se encontraron estudiantes inscritos.")

except Exception as e:
    test_passed = False
    with open("screenshots/CP-RF-0015-A.log", "w", encoding="utf-8") as log_file:
        log_file.write(f"Error: {str(e)}\n")
    driver.save_screenshot(SCREENSHOT_PATH_ERROR)

finally:
    time.sleep(2)
    if test_passed:
        driver.save_screenshot(SCREENSHOT_PATH_SUCCESS)
    print("✅ Caso de prueba ejecutado exitosamente. Ver resultados en la evidencia.")
    driver.quit()
