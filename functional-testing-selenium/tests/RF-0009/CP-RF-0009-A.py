import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
try:
    from driver_setup import get_driver_for_rf
    from common_helpers import take_screenshot
except ImportError:
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

# Constantes del caso de prueba
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search"
SEARCH_SUBSTRING = "Ana"
EXPECTED_SUBSTRING = "Ana"

def wait_for_search_box(driver):
    """Esperar a que el cuadro de búsqueda esté disponible"""
    try:
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-keyword")))
        return search_box
    except Exception:
        return None

def click_search_button(driver):
    """Hace clic en el botón Search si existe"""
    try:
        search_btn = driver.find_element(By.ID, "btn-search")
        search_btn.click()
        return True
    except Exception:
        return False

def perform_search(driver, substring):
    """Ingresar el substring y ejecutar la búsqueda"""
    search_box = wait_for_search_box(driver)
    if not search_box:
        print("No se encontró el cuadro de búsqueda.")
        return False
    search_box.clear()
    search_box.send_keys(substring)
    take_screenshot(driver, "CP-RF-0009-A", "01-busqueda-ingresada")
    # Pulsar Enter o botón Search
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    click_search_button(driver)
    time.sleep(3)
    return True

def get_visible_student_names(driver):
    """
    Obtiene los nombres de los estudiantes visibles en todas las tablas de resultados.
    Busca todas las tablas dentro de divs con clase 'student-course-table' y extrae el nombre de la tercera columna.
    """
    names = []
    try:
        tables = driver.find_elements(By.CSS_SELECTOR, "div.student-course-table table")
        for table in tables:
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:
                    name = cells[2].text.strip()
                    if name:
                        names.append(name)
    except Exception as e:
        print(f"Error al obtener nombres: {e}")
    return names

def verify_search_results(driver, expected_substring):
    """
    Verifica los criterios de aceptación:
    1. Se muestran todas las coincidencias posibles con el nombre.
    2. Al menos uno.
    3. UI sin errores (no se detectan errores visibles).
    """
    names = get_visible_student_names(driver)
    print(f"Nombres encontrados en la tabla: {names}")

    # 1. Al menos una coincidencia
    if not names:
        print("TEST CP-RF-0009-A: FALLIDO - No se encontró ningún estudiante.")
        return False

    # 2. Todas las coincidencias contienen el substring buscado (case-insensitive)
    coincidencias = [n for n in names if expected_substring.lower() in n.lower()]
    if len(coincidencias) != len(names):
        print("TEST CP-RF-0009-A: FALLIDO - Hay estudiantes que no contienen el substring buscado.")
        return False

    # 3. Verificar que no hay errores de UI (alert-danger, error, etc.)
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error, .has-error")
    if error_elements:
        print("TEST CP-RF-0009-A: FALLIDO - Se detectaron errores en la UI.")
        return False

    print("TEST CP-RF-0009-A: EXITOSO - Todas las coincidencias contienen el substring y la UI está limpia.")
    return True

def test_busqueda_por_nombre():
    print("CP-RF-0009-A: Búsqueda por nombre")
    print("Requisito: RF-0009 – Buscar Estudiante en Curso")
    print("Técnica: Partición de equivalencia")
    print(f"Entrada: Cuadro de búsqueda → {SEARCH_SUBSTRING}")
    print(f"Link de caso de prueba: {TEST_URL}")
    print("Criterios de aceptación:")
    print("1. Se muestran todas las coincidencias posibles con el nombre.")
    print("2. Al menos uno.")
    print("3. UI sin errores.\n")

    driver = None
    try:
        driver = get_driver_for_rf("0009")
        wait = WebDriverWait(driver, 10)
        driver.get(TEST_URL)
        time.sleep(3)

        if not perform_search(driver, SEARCH_SUBSTRING):
            return False

        take_screenshot(driver, "CP-RF-0009-A", "02-despues-busqueda")

        return verify_search_results(driver, EXPECTED_SUBSTRING)

    except Exception as e:
        print(f"ERROR en CP-RF-0009-A: {e}")
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0009-A", "error-critico")
        except Exception:
            pass
        return False
    finally:
        if driver:
            try:
                print("🧹 Cerrando navegador...")
                driver.quit()
            except Exception:
                pass

def main():
    print("SUITE DE PRUEBAS RF-0009")
    print("Caso: CP-RF-0009-A - Búsqueda por nombre")
    print("=" * 60)
    result = test_busqueda_por_nombre()
    print("\n" + "=" * 60)
    if result:
        print("RESULTADO FINAL: EXITOSO")
    else:
        print("RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    return result

if __name__ == "__main__":
    main()