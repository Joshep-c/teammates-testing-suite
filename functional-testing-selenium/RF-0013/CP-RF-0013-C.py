import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Asegurar acceso a módulos del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "PS-B"  # ID de curso activo

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")

wait = WebDriverWait(driver, 10)

try:
    # Paso 1: Buscar el curso en "Active Courses"
    print(f"🔎 Buscando curso activo con ID: {COURSE_ID}...")
    course_row = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]"
    )))
    print("✅ Curso activo encontrado.")

    # Paso 2: Clic en “Other Actions”
    other_actions_button = course_row.find_element(By.XPATH, ".//button[contains(text(), 'Other Actions')]")
    other_actions_button.click()
    print("📂 Menú 'Other Actions' desplegado.")

    # Esperar que se renderice el menú
    time.sleep(1)

    # Paso 3: Verificar que NO existe botón “Unarchive”
    try:
        course_row.find_element(By.XPATH, ".//button[contains(text(), 'Unarchive')]")
        print("❌ ERROR: Botón 'Unarchive' está visible en un curso activo.")
    except:
        print("✅ Confirmado: Botón 'Unarchive' no está presente en curso activo.")

    # Captura de pantalla
    driver.save_screenshot("screenshots/IMG-1-CP-RF-0013-C.png")
    print("📸 Captura guardada: IMG-1-CP-RF-0013-C.png")

except Exception as e:
    print("❌ Error durante la verificación:", e)

time.sleep(3)
driver.quit()
