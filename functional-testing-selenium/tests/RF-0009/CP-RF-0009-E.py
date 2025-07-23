import sys
import os
import time

# Añadir utilidades al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
try:
    from driver_setup import get_driver_for_rf
    from common_helpers import take_screenshot
except ImportError:
    def get_driver_for_rf(_):
        from selenium import webdriver
        return webdriver.Chrome()
    def take_screenshot(driver, test_name, screenshot_name):
        path = f"{test_name}_{screenshot_name}.png"
        driver.save_screenshot(path)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Constantes del caso CP-RF-0009-E
TEST_ID = "CP-RF-0009-E"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
SEARCH_TERM = "Zyxwvu"


def wait_for_search_box(driver):
    try:
        return WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search-keyword"))
        )
    except:
        return None


def click_search_button(driver):
    try:
        driver.find_element(By.ID, "btn-search").click()
        return True
    except:
        return False


def perform_search(driver, query):
    box = wait_for_search_box(driver)
    if not box:
        print(f"{TEST_ID}: FALLIDO - No se encontró el cuadro de búsqueda.")
        return False
    box.clear()
    box.send_keys(query)
    take_screenshot(driver, TEST_ID, "01-input")
    box.send_keys(Keys.ENTER)
    click_search_button(driver)
    return True


def wait_for_no_results(driver):
    """Espera aparición del mensaje de 'No results found.'"""
    try:
        toast = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast-body"))
        )
        return toast
    except:
        return None


def test_sin_resultados():
    print(f"Iniciando caso {TEST_ID}: Sin resultados para '{SEARCH_TERM}'")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)

        if not perform_search(driver, SEARCH_TERM):
            return False

        toast = wait_for_no_results(driver)
        if not toast:
            print(f"{TEST_ID}: FALLIDO - No apareció mensaje de 'No results found.'")
            take_screenshot(driver, TEST_ID, "no-toast")
            return False

        # Captura la pantalla mostrando el mensaje de no resultados
        take_screenshot(driver, TEST_ID, "02-no-results")

        toast_text = toast.text.strip()
        print(f"Mensaje mostrado: {toast_text}")
        if toast_text != "No results found.":
            print(f"{TEST_ID}: FALLIDO - Texto inesperado: '{toast_text}'")
            return False

        # Verificar que no haya errores en la UI
        errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
        if errors:
            print(f"{TEST_ID}: FALLIDO - Errores visibles en UI.")
            return False

        print(f"{TEST_ID}: EXITOSO - Se mostró correctamente el mensaje 'No results found.' sin errores.")
        return True

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
    print("=" * 60)
    result = test_sin_resultados()
    print("=" * 60)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("=" * 60)
    return result

if __name__ == "__main__":
    main()
