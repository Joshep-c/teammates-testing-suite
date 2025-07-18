import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "PS-B"

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Expandir sección 'Archived Courses'
    print("🔍 Expandir sección 'Archived Courses'...")
    archived_toggle = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class,'chevron')]")
    ))
    archived_toggle.click()
    print("✅ Panel 'Archived Courses' expandido.")

    time.sleep(1)

    # Paso 2: Verificar que curso archivado está presente
    archived_course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]")
    ))
    print("✅ Curso archivado encontrado.")

    # Paso 3: Validar que no tenga botones de gestión activos (Other Actions, Edit, View)
    try:
        archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Other Actions')]")
        print("❌ ERROR: Botón 'Other Actions' aún presente.")
    except:
        print("✅ Botón 'Other Actions' NO presente.")

    try:
        archived_course_row.find_element(By.XPATH, ".//a[contains(text(), 'Edit')]")
        print("❌ ERROR: Opción 'Edit' aún presente.")
    except:
        print("✅ Opción 'Edit' NO presente.")

    try:
        archived_course_row.find_element(By.XPATH, ".//a[contains(text(), 'View')]")
        print("❌ ERROR: Opción 'View' aún presente.")
    except:
        print("✅ Opción 'View' NO presente.")

    # Paso 4: Verificar que tenga botones 'Unarchive' y 'Delete'
    unarchive_btn = archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Unarchive')]")
    delete_btn = archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")

    if unarchive_btn and delete_btn:
        print("🗃 Botones 'Unarchive' y 'Delete' detectados correctamente. ✅")
        driver.save_screenshot("screenshots/IMG-1-CP-RF-0012-B.png")
    else:
        print("❌ Botones esperados no encontrados.")

except Exception as e:
    print("❌ Error durante la validación de estado archivado:", e)

time.sleep(3)
driver.quit()
