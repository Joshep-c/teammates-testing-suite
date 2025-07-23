import sys
import os
import time

# Añadir utilidades al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
try:
    from driver_setup import get_driver_for_rf
    from common_helpers import take_screenshot
except ImportError:
    # Fallback en caso de no encontrar los módulos utilitarios
    def get_driver_for_rf(_):
        from selenium import webdriver
        return webdriver.Chrome()

    def take_screenshot(driver, test_name, screenshot_name):
        screenshot_path = f"{test_name}_{screenshot_name}.png"
        driver.save_screenshot(screenshot_path)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Constantes del caso CP-RF-0009-B
TEST_ID = "CP-RF-0009-B"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
SEARCH_EMAIL = "anaoconnortest@ejemplo.com"


def wait_for_search_box(driver):
    """Espera el cuadro de búsqueda"""
    try:
        return WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search-keyword"))
        )
    except Exception:
        return None


def click_search_button(driver):
    """Hace clic en el botón de búsqueda"""
    try:
        btn = driver.find_element(By.ID, "btn-search")
        btn.click()
        return True
    except Exception:
        return False


def perform_search(driver, query):
    """Ingresa el correo y ejecuta la búsqueda"""
    box = wait_for_search_box(driver)
    if not box:
        print(f"{TEST_ID}: FALLIDO - No se encontró el cuadro de búsqueda.")
        return False
    box.clear()
    box.send_keys(query)
    take_screenshot(driver, TEST_ID, "01-input")
    box.send_keys(Keys.ENTER)
    time.sleep(1)
    click_search_button(driver)
    time.sleep(3)
    return True


def get_visible_student_emails(driver):
    """Extrae los correos desde la quinta columna de cada fila"""
    emails = []
    try:
        tables = driver.find_elements(By.CSS_SELECTOR, "div.student-course-table table")
        for table in tables:
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                # La columna de correo es la quinta (índice 4)
                if len(cells) >= 5:
                    text = cells[4].text.strip()
                    if text:
                        emails.append(text)
    except Exception as e:
        print(f"Error al obtener correos: {e}")
    return emails


def verify_search_by_email(driver, expected_email):
    """Verifica coincidencia exacta de correo y ausencia de errores UI"""
    emails = get_visible_student_emails(driver)
    print(f"Correos encontrados: {emails}")

    if not emails:
        print(f"{TEST_ID}: FALLIDO - No se encontró ningún correo.")
        return False

    # Coincidencia exacta ignorando mayúsculas/minúsculas
    matches = [e for e in emails if e.lower() == expected_email.lower()]
    if not matches:
        print(f"{TEST_ID}: FALLIDO - No hay coincidencia exacta para '{expected_email}'.")
        return False
    if len(matches) != len(emails):
        print(f"{TEST_ID}: FALLIDO - Aparecen correos adicionales no esperados.")
        return False

    # Verificar que no hay errores visibles en UI
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
    if error_elements:
        print(f"{TEST_ID}: FALLIDO - Se detectaron errores en la UI.")
        return False

    print(f"{TEST_ID}: EXITOSO - Búsqueda por correo correcta.")
    return True


def test_busqueda_por_correo():
    print(f"Iniciando caso {TEST_ID}: Búsqueda por correo exacto")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)
        time.sleep(3)

        if not perform_search(driver, SEARCH_EMAIL):
            return False

        take_screenshot(driver, TEST_ID, "02-after-search")
        return verify_search_by_email(driver, SEARCH_EMAIL)

    except Exception as e:
        print(f"ERROR en {TEST_ID}: {e}")
        if driver:
            take_screenshot(driver, TEST_ID, "error")
        return False

    finally:
        if driver:
            try:
                print("🧹 Cerrando navegador...")
                driver.quit()
            except:
                pass


def main():
    print("SUITE DE PRUEBAS RF-0009")
    print("=" * 50)
    result = test_busqueda_por_correo()
    print("=" * 50)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("=" * 50)
    return result


if __name__ == "__main__":
    main()
