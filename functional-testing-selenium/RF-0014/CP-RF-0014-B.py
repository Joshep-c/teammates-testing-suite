import sys
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.driver_setup import get_driver

COURSE_ID = "CS303"
SCREENSHOT_PATH = "screenshots/IMG-1-CP-RF-0014-B.png"

driver = get_driver()
driver.get("https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses")
wait = WebDriverWait(driver, 10)

try:
    print("🔐 Caso de Prueba CP-RF-0014-B: Eliminación desde Active Courses")

    # Paso 1: Buscar la fila del curso activo
    print(f"🔍 Buscando curso activo con ID: {COURSE_ID}...")
    course_row = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]"
    )))
    print("✅ Curso activo encontrado.")

    # Paso 2: Buscar y hacer clic en el botón 'Other Actions'
    print("🧭 Abriendo menú 'Other Actions'...")
    other_actions_button = course_row.find_element(By.XPATH, ".//button[contains(., 'Other Actions')]")
    driver.execute_script("arguments[0].click();", other_actions_button)  # Usa JS por si el botón no responde a .click()
    time.sleep(1)  # Espera breve para que se despliegue el menú

    # Paso 3: Hacer clic en la opción 'Delete'
    print("🗑 Haciendo clic en 'Delete'...")
    delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Delete')]")))
    driver.execute_script("arguments[0].click();", delete_button)
    
    # Paso 4: Confirmar eliminación
    print("📋 Confirmando eliminación (clic en 'Yes')...")
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes')]")))
    confirm_button.click()

    # Paso 5: Verificar que el curso ya no aparece en la lista
    print("⌛ Esperando que el curso sea eliminado de la lista...")
    wait.until_not(EC.presence_of_element_located((
        By.XPATH, f"//table//tr[td[contains(text(), '{COURSE_ID}')]]"
    )))
    print("✅ Curso eliminado correctamente de 'Active Courses'.")

    # Paso 6: Captura de pantalla
    driver.save_screenshot(SCREENSHOT_PATH)
    print(f"📸 Captura guardada: {SCREENSHOT_PATH}")

except Exception as e:
    print("❌ Error durante el caso de prueba CP-RF-0014-B:", e)
    driver.save_screenshot("screenshots/error_CP-RF-0014-B.png")

finally:
    time.sleep(2)
    driver.quit()
