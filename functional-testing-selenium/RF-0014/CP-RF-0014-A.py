import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Acceso al setup del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "PS-B"  # ID del curso a eliminar

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Expandir panel Archived Courses si es necesario
    print("📂 Expandir panel 'Archived Courses'...")
    chevron = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class, 'chevron')]"
    )))
    chevron.click()
    print("✅ Panel expandido.")

    # Paso 2: Esperar a que cargue el curso archivado
    print(f"🔍 Buscando curso archivado con ID: {COURSE_ID}...")
    archived_row = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]"
    )))
    print("📌 Curso archivado encontrado.")

    # Paso 3: Clic en “Other Actions”
    other_actions_btn = archived_row.find_element(By.XPATH, ".//button[contains(text(), 'Other Actions')]")
    other_actions_btn.click()
    print("☑️ Menú 'Other Actions' abierto.")

    # Pausa para asegurar despliegue del menú
    time.sleep(1)

    # Paso 4: Click en botón “Delete”
    delete_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(text(), 'Delete')]"
    )))
    delete_button.click()
    print("🗑 Botón 'Delete' presionado.")

    # Paso 5: Confirmar desaparición del curso
    time.sleep(2)  # Esperamos que se actualice la tabla
    try:
        wait.until_not(EC.presence_of_element_located((
            By.XPATH, f"//table//td[contains(text(), '{COURSE_ID}')]"
        )))
        print("✅ Curso eliminado correctamente. Ya no aparece en 'Archived Courses'.")
    except:
        print("❌ El curso aún aparece en 'Archived Courses'.")

    # Captura de pantalla del estado final
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0014-A.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0014-A.png")

except Exception as e:
    print("❌ Error durante la eliminación del curso:", e)

time.sleep(3)
driver.quit()
