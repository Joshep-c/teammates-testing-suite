import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "PS-B"
SCREENSHOT_PATH = "screenshots/IMG-1-CP-RF-0014-A.png"

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")
wait = WebDriverWait(driver, 10)

try:
    print("🔐 Caso de Prueba CP-RF-0014-A: Eliminación de curso archivado")

    # Paso 1: Expandir sección 'Archived Courses'
    print("📂 Buscando sección 'Archived Courses'...")
    archived_toggle = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[@id='archived-table-heading']//button[contains(@class,'chevron')]"
    )))
    archived_toggle.click()
    print("✅ Panel expandido.")
    time.sleep(1)

    # Paso 2: Buscar el curso archivado
    print(f"🔎 Buscando curso archivado '{COURSE_ID}'...")
    archived_course_row = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]"
    )))
    print("📌 Curso encontrado.")

    # Paso 3: Presionar botón Delete
    print("🗑 Presionando botón 'Delete'...")
    delete_button = archived_course_row.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
    delete_button.click()
    print("✅ Botón 'Delete' presionado.")

    # Paso 4: Confirmar en el modal de confirmación (clic en "Yes")
    print("🧾 Esperando ventana de confirmación...")
    confirm_yes_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(text(), 'Yes')]"
    )))
    confirm_yes_button.click()
    print("🟢 Confirmación aceptada ('Yes' presionado).")

    # Paso 5: Esperar que desaparezca de 'Archived Courses'
    print("⌛ Confirmando que el curso fue eliminado...")
    wait.until_not(EC.presence_of_element_located((
        By.XPATH, f"//div[@id='archived-table']//td[contains(text(), '{COURSE_ID}')]"
    )))
    print("✅ Curso eliminado correctamente. Ya no está en 'Archived Courses'.")

    # Paso 6: Captura de pantalla final
    driver.save_screenshot(SCREENSHOT_PATH)
    print(f"📸 Captura guardada: {SCREENSHOT_PATH}")

except Exception as e:
    print("❌ Error durante el caso de prueba CP-RF-0014-A:", e)

finally:
    time.sleep(2)
    driver.quit()
