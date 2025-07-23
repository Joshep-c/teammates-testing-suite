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

# Constantes del caso CP-RF-0009-F
TEST_ID = "CP-RF-0009-F"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
# Cadena de 100 'A'
SEARCH_STRING = "A" * 100
COUNTER_SELECTOR = "div.form-group span"


def wait_for_search_box(driver):
    try:
        return WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search-keyword"))
        )
    except:
        return None


def perform_length_test(driver, input_box):
    # Ingresar 100 caracteres
    input_box.clear()
    input_box.send_keys(SEARCH_STRING)
    time.sleep(0.5)
    take_screenshot(driver, TEST_ID, "01-full-input")

    # Verificar contador
    counter = driver.find_element(By.CSS_SELECTOR, COUNTER_SELECTOR).text.strip()
    print(f"Counter after 100 chars: {counter}")
    if counter.lower() != "0 characters left":
        print(f"{TEST_ID}: FALLIDO - Contador incorrecto: '{counter}'")
        return False

    # Intentar escribir uno más
    input_box.send_keys("B")
    time.sleep(0.2)
    value = input_box.get_attribute("value")
    length = len(value)
    print(f"Length after extra char: {length}")
    if length != 100:
        print(f"{TEST_ID}: FALLIDO - Se permitieron más de 100 caracteres")
        return False

    take_screenshot(driver, TEST_ID, "02-length-verified")
    return True


def click_search(driver):
    try:
        btn = driver.find_element(By.ID, "btn-search")
        btn.click()
    except:
        pass


def wait_for_results(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.student-course-table table tbody tr"))
        )
        return True
    except:
        return False


def get_visible_student_names(driver):
    names = []
    rows = driver.find_elements(By.CSS_SELECTOR, "div.student-course-table table tbody tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            names.append(cells[2].text.strip())
    return names


def test_longitud_maxima():
    print(f"Iniciando caso {TEST_ID}: Longitud máxima del campo")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)

        box = wait_for_search_box(driver)
        if not box:
            print(f"{TEST_ID}: FALLIDO - No se encontró el cuadro de búsqueda.")
            return False

        # 1 y 2: longitud y contador
        if not perform_length_test(driver, box):
            return False

        # 3: búsqueda y verificación de coincidencia exacta
        box.clear()
        box.send_keys(SEARCH_STRING)
        click_search(driver)
        if not wait_for_results(driver):
            print(f"{TEST_ID}: FALLIDO - No se cargaron resultados.")
            return False
        take_screenshot(driver, TEST_ID, "03-after-search")

        names = get_visible_student_names(driver)
        print(f"Nombres encontrados: {names}")
        if SEARCH_STRING not in names:
            print(f"{TEST_ID}: FALLIDO - No se encontró la cadena de 100 caracteres en resultados.")
            return False

        # Verificar sin errores UI
        errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
        if errors:
            print(f"{TEST_ID}: FALLIDO - Errores visibles en UI.")
            return False

        print(f"{TEST_ID}: EXITOSO - Longitud máxima validada y coincidencia encontrada.")
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
    result = test_longitud_maxima()
    print("=" * 60)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("=" * 60)
    return result

if __name__ == "__main__":
    main()
