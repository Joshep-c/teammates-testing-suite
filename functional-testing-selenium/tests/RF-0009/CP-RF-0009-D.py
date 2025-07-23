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

# Constantes del caso CP-RF-0009-D
TEST_ID = "CP-RF-0009-D"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
# Entrada literal con comillas para ejecutar búsqueda
SEARCH_PHRASE = '"Alice Betsy"'
# Nombre esperado sin comillas para comparar
EXPECTED_NAME = SEARCH_PHRASE.strip('"')


def wait_for_search_box(driver):
    try:
        return WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search-keyword"))
        )
    except:
        return None


def click_search_button(driver):
    try:
        btn = driver.find_element(By.ID, "btn-search")
        btn.click()
        return True
    except:
        return False


def wait_for_results(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.student-course-table table tbody tr"))
        )
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
    if not wait_for_results(driver):
        print(f"{TEST_ID}: FALLIDO - No se cargaron resultados en el tiempo esperado.")
        return False
    take_screenshot(driver, TEST_ID, "02-results")
    return True


def get_visible_student_names(driver):
    names = []
    rows = driver.find_elements(By.CSS_SELECTOR, "div.student-course-table table tbody tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            text = cells[2].text.strip()
            if text:
                names.append(text)
    return names


def verify_exact_phrase(names):
    print(f"Nombres encontrados: {names}")
    # 1. Al menos un resultado esperado
    if not names:
        print(f"{TEST_ID}: FALLIDO - No se encontró ningún estudiante con frase exacta.")
        return False
    # 2. Todos deben coincidir exactamente con EXPECTED_NAME
    mismatches = [n for n in names if n.lower() != EXPECTED_NAME.lower()]
    if mismatches:
        print(f"{TEST_ID}: FALLIDO - Resultados extra o incorrectos: {mismatches}")
        return False
    print(f"{TEST_ID}: EXITOSO - Solo se mostraron registros exactos '{EXPECTED_NAME}'.")
    return True


def test_busqueda_frase_exacta():
    print(f"Iniciando caso {TEST_ID}: Búsqueda de frase exacta {SEARCH_PHRASE}")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)
        time.sleep(2)
        if not perform_search(driver, SEARCH_PHRASE):
            return False
        names = get_visible_student_names(driver)
        if not verify_exact_phrase(names):
            return False
        # Verificar ausencia de errores UI
        errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
        if errors:
            print(f"{TEST_ID}: FALLIDO - Errores visibles en UI.")
            return False
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
    print("="*60)
    result = test_busqueda_frase_exacta()
    print("="*60)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("="*60)
    return result

if __name__ == "__main__":
    main()
