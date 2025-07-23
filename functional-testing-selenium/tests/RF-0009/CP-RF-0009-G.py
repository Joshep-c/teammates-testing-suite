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

# Constantes del caso CP-RF-0009-G
TEST_ID = "CP-RF-0009-G"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
# Cadena de 101 'A'
LONG_STRING = "A" * 101
COUNTER_SELECTOR = "div.form-group span"


def wait_for_search_box(driver):
    try:
        return WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search-keyword"))
        )
    except:
        return None


def test_excede_longitud():
    print(f"Iniciando caso {TEST_ID}: Excede longitud máxima")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)

        box = wait_for_search_box(driver)
        if not box:
            print(f"{TEST_ID}: FALLIDO - No se encontró el cuadro de búsqueda.")
            return False

        # Intentar ingresar 101 caracteres
        box.clear()
        box.send_keys(LONG_STRING)
        time.sleep(0.5)

        # Verificar que no se hayan añadido más de 100 caracteres
        value = box.get_attribute("value")
        length = len(value)
        print(f"Longitud real en el campo: {length}")
        if length != 100:
            print(f"{TEST_ID}: FALLIDO - Permitió {length} caracteres, más del máximo permitido.")
            take_screenshot(driver, TEST_ID, "error-length")
            return False

        # Verificar contador
        counter = driver.find_element(By.CSS_SELECTOR, COUNTER_SELECTOR).text.strip()
        print(f"Counter: {counter}")
        if counter.lower() != "0 characters left":
            print(f"{TEST_ID}: FALLIDO - Contador inconsistente: '{counter}'")
            take_screenshot(driver, TEST_ID, "error-counter")
            return False

        # Captura de pantalla para evidenciar la restricción
        take_screenshot(driver, TEST_ID, "01-max-length")

        print(f"{TEST_ID}: EXITOSO - No se permitieron más de 100 caracteres y UI consistente.")
        return True

    except Exception as e:
        print(f"ERROR en {TEST_ID}: {e}")
        if driver:
            take_screenshot(driver, TEST_ID, "error-exception")
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
    result = test_excede_longitud()
    print("=" * 60)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("=" * 60)
    return result

if __name__ == "__main__":
    main()
