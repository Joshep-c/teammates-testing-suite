import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "PS-B"

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Expandir panel de 'Archived Courses'
    print("📂 Buscando sección 'Archived Courses'...")
    archived_toggle = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class,'chevron')]")
    ))
    archived_toggle.click()
    print("✅ Panel 'Archived Courses' expandido.")

    time.sleep(1)

    # Paso 2: Localizar curso archivado
    archived_course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]")
    ))
    print(f"📌 Curso archivado '{COURSE_ID}' encontrado.")

    # Paso 3: Clic en botón "Unarchive"
    unarchive_button = archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Unarchive')]")
    unarchive_button.click()
    print("♻ Botón 'Unarchive' presionado.")

    # Paso 4: Esperar a que desaparezca de archivados
    wait.until_not(EC.presence_of_element_located(
        (By.XPATH, f"//div[@id='archived-table']//td[contains(text(), '{COURSE_ID}')]")
    ))
    print("✅ Curso ya no aparece en 'Archived Courses'.")

    # Paso 5: Validar que reaparezca en 'Active Courses'
    active_course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//td[contains(text(), '{COURSE_ID}')]")
    ))
    print("🎉 Curso restaurado correctamente y visible en 'Active Courses'. ✅")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0013-A.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0013-A.png")

except Exception as e:
    print("❌ Error durante la restauración del curso:", e)

time.sleep(3)
driver.quit()
