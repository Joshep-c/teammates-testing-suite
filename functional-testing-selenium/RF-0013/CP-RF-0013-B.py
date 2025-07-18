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
    # Paso 1: Expandir sección Archived Courses
    print("📂 Expandir panel 'Archived Courses'...")
    archived_toggle = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class,'chevron')]")
    ))
    archived_toggle.click()
    print("✅ Panel expandido.")

    time.sleep(1)

    # Paso 2: Ubicar curso y presionar "Unarchive"
    archived_course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]")
    ))
    print("📌 Curso archivado encontrado.")

    unarchive_button = archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Unarchive')]")
    unarchive_button.click()
    print("♻ Botón 'Unarchive' presionado.")

    # Paso 3: Esperar que desaparezca de archivados
    wait.until_not(EC.presence_of_element_located(
        (By.XPATH, f"//div[@id='archived-table']//td[contains(text(), '{COURSE_ID}')]")
    ))
    print("✅ Curso ya no está en 'Archived Courses'.")

    # Paso 4: Confirmar que aparece en Active Courses y es gestionable
    active_course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]")
    ))
    print("📋 Curso visible nuevamente en 'Active Courses'.")

    # Confirmar presencia del botón 'Other Actions'
    other_actions_button = active_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Other Actions')]")
    assert other_actions_button.is_displayed(), "❌ El botón 'Other Actions' no está visible"
    print("✅ Curso gestionable nuevamente. Transición de estado confirmada. 🎯")

    # Captura de evidencia
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0013-B.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0013-B.png")

except Exception as e:
    print("❌ Error en la verificación del cambio de estado:", e)

time.sleep(3)
driver.quit()
