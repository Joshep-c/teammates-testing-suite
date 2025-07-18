import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.driver_setup import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

COURSE_ID = "PS-B"

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")
wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Buscar el curso en la tabla
    print(f"🔍 Buscando curso activo con ID: {COURSE_ID}...")
    course_row = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]")
    ))
    print("✅ Curso activo encontrado.")

    # Paso 2: Clic en "Other Actions"
    other_actions_button = course_row.find_element(By.XPATH, ".//button[contains(text(), 'Other Actions')]")
    other_actions_button.click()
    print("✅ Botón 'Other Actions' presionado.")

    # Paso 3: Esperar y hacer clic en "Archive"
    time.sleep(0.5)  # Pequeña pausa para que el menú se despliegue

    archive_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-archive-1")))
    archive_button.click()
    print("📦 Botón 'Archive' presionado.")

    # Paso 4: Esperar a que desaparezca de "Active Courses"
    time.sleep(2)
    try:
        wait.until_not(EC.presence_of_element_located(
            (By.XPATH, f"//table//td[contains(text(), '{COURSE_ID}')]")
        ))
        print("✅ Curso ya no está en 'Active Courses'.")
    except:
        print("❌ El curso aún aparece en 'Active Courses'.")

    # Paso 5: Expandir la sección 'Archived Courses'
    try:
        print("📁 Buscando panel 'Archived Courses' para expandirlo...")
        archived_panel_toggle = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class, 'chevron')]")
        ))
        archived_panel_toggle.click()
        print("🔽 Panel 'Archived Courses' expandido.")
    except Exception as e:
        print("❌ No se pudo expandir el panel de cursos archivados:", e)
        driver.save_screenshot("screenshots/error_expand_archived.png")
        raise e

    # Paso 6: Verificar que el curso archivado aparece en la lista
    try:
        archived_course = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//table//td[contains(text(), '{COURSE_ID}')]")
        ))
        print("🎉 Curso archivado correctamente y visible en 'Archived Courses'. ✅")
        driver.save_screenshot("screenshots/IMG-1-CP-RF-0012-A.png")
    except Exception as e:
        print("❌ No se encontró el curso en 'Archived Courses':", e)
        driver.save_screenshot("screenshots/error_archived_course_not_found.png")
        raise e

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0012-A.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0012-A.png")

except Exception as e:
    print("❌ Error durante el flujo de archivado:", e)

time.sleep(3)
driver.quit()
