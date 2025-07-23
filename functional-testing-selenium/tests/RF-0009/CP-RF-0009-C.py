import sys
import os
import time

# Añadir utilidades al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
try:
    from driver_setup import get_driver_for_rf
    from common_helpers import take_screenshot
except ImportError:
    # Fallback en caso de no encontrar utilitarios
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

# Constantes del caso CP-RF-0009-C
TEST_ID = "CP-RF-0009-C"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
# Input literal incluyendo las comillas
SEARCH_SECTION = '"Tutorial Group 2"'
# Para comparar con el texto real en la celda (sin comillas)
EXPECTED_SECTION = SEARCH_SECTION.strip('"')


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
        print(f"{TEST_ID}: FALLIDO - No se cargaron resultados en 15s.")
        return False
    take_screenshot(driver, TEST_ID, "02-results")
    return True


def get_sections(driver):
    sections = []
    rows = driver.find_elements(By.CSS_SELECTOR, "div.student-course-table table tbody tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            text = cells[0].text.strip()
            if text:
                sections.append(text)
    return sections


def verify_sections(sections):
    print(f"Secciones encontradas: {sections}")
    if not sections:
        print(f"{TEST_ID}: FALLIDO - No se encontraron filas.")
        return False

    # Todas deben coincidir exactamente con EXPECTED_SECTION
    mismatches = [s for s in sections if s.lower() != EXPECTED_SECTION.lower()]
    if mismatches:
        print(f"{TEST_ID}: FALLIDO - Coincidencias inesperadas: {mismatches}")
        return False
    return True


def test_busqueda_por_seccion():
    print(f"Iniciando caso {TEST_ID}: Búsqueda por sección {SEARCH_SECTION}")
    driver = None
    try:
        driver = get_driver_for_rf(TEST_ID)
        driver.get(TEST_URL)

        if not perform_search(driver, SEARCH_SECTION):
            return False

        sections = get_sections(driver)
        if not verify_sections(sections):
            return False

        # Verificar ausencia de errores UI
        errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
        if errors:
            print(f"{TEST_ID}: FALLIDO - Errores visibles en UI.")
            return False

        print(f"{TEST_ID}: EXITOSO - Todas las filas corresponden a {SEARCH_SECTION}.")
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
    result = test_busqueda_por_seccion()
    print("="*60)
    print(f"RESULTADO FINAL: {'EXITOSO' if result else 'FALLIDO'}")
    print("="*60)
    return result

if __name__ == "__main__":
    main()
