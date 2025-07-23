import sys
import os
import time

# Agregar el path para usar la estructura global util
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
try:
    from driver_setup import get_driver_for_rf
    from common_helpers import take_screenshot
except ImportError:
    # Fallback para importaciones
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
from selenium.webdriver.common.action_chains import ActionChains

# Constantes
SCROLL_SCRIPT = "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses"
STUDENT_DATA = {
    "name": "Carlos López",
    "section": "",  # Sección vacía - caso de prueba
    "team": "",     # Equipo vacío - caso de prueba
    "email": "carlos.lopez@unsa.edu.pe",
    "comments": "Campos Section y Team vacíos"
}

# Funciones principales simplificadas
def wait_for_table_ready(driver):
    """Esperar a que la tabla de enrollment esté lista - manteniendo scroll arriba"""
    try:
        wait = WebDriverWait(driver, 15)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        if table.is_displayed():
            time.sleep(3)
            # Mantener scroll en la parte superior para ver mensajes de error
            driver.execute_script("window.scrollTo(0, 0);")
            return True
    except Exception:
        time.sleep(5)
    return True

def handle_teammates_enrollment_form(driver):
    """Verificar que la tabla de Handsontable esté lista"""
    try:
        gridcells = driver.find_elements(By.CSS_SELECTOR, 'td[role="gridcell"]')
        return len(gridcells) > 0
    except Exception:
        return False

def fill_handsontable_data(driver, student_data):
    """Llenar datos en tabla Handsontable de TEAMMATES"""
    try:
        gridcells = driver.find_elements(By.CSS_SELECTOR, 'td[role="gridcell"]')
        if not gridcells:
            return False
        
        # Mapeo de campos a columnas: Section - Team - Name - Email - Comments
        field_to_column = {
            "section": 1, "team": 2, "name": 3, "email": 4, "comments": 5
        }
        
        table_container = driver.find_element(By.XPATH, "//table[.//td[@role='gridcell']]")
        fields_filled = 0
        
        for field_name, column_index in field_to_column.items():
            value = student_data.get(field_name, "")
            
            # Para este caso específico, section y team deben quedar vacíos
            if field_name in ["section", "team"]:
                value = ""
            
            xpath_options = [
                f".//tbody/tr[1]/td[{column_index}][@role='gridcell']",
                f".//tr[1]/td[{column_index}][@role='gridcell']",
                f"(.//td[@role='gridcell'])[{column_index}]"
            ]
            
            for xpath in xpath_options:
                try:
                    cell = table_container.find_element(By.XPATH, xpath)
                    if cell.is_displayed():
                        driver.execute_script(SCROLL_SCRIPT, cell)
                        time.sleep(0.5)
                        
                        actions = ActionChains(driver)
                        actions.double_click(cell).perform()
                        time.sleep(1)
                        
                        try:
                            edit_input = driver.find_element(By.CSS_SELECTOR, "input.handsontableInput")
                            edit_input.clear()
                            if value:  # Solo enviar si hay valor
                                edit_input.send_keys(value)
                            edit_input.send_keys(Keys.ENTER)
                        except Exception:
                            if value:
                                actions.send_keys(value).perform()
                            actions.send_keys(Keys.ENTER).perform()
                        
                        if field_name not in ["section", "team"]:  # Solo contar campos que no sean section/team
                            fields_filled += 1
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        
        return fields_filled >= 2  # Esperamos al menos nombre y email
    except Exception:
        return False

def fill_student_data_teammates_mejorado(driver, student_data):
    """Ingresar datos del estudiante usando Handsontable"""
    if not handle_teammates_enrollment_form(driver):
        return False
    
    return fill_handsontable_data(driver, student_data)

def verify_section_team_errors(driver):
    """Verificar errores específicos para campos Section y Team vacíos"""
    result = {"success": False, "messages": [], "errors": []}
    
    # Buscar errores específicos para section y team vacíos (basado en los patrones reales)
    section_team_error_patterns = [
        "Found empty compulsory fields",
        "empty compulsory fields", 
        "Section Name is required",
        "Section is required", 
        "Team Name is required",
        "Team is required",
        "Section cannot be empty",
        "Team cannot be empty",
        "Section field is mandatory",
        "Team field is mandatory",
        "compulsory fields",
        "failed to be enrolled"
    ]
    
    # Buscar errores en elementos comunes, incluyendo específicamente bg-danger
    error_selectors = [
        ".bg-danger", "div.bg-danger", ".card-body.bg-danger",
        ".card-header.bg-danger", "td", ".enroll-results-panel",
        ".error", ".alert-danger", "*[class*='error']", 
        ".invalid-feedback", ".text-danger", "*[class*='invalid']"
    ]
    
    for selector in error_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        # Solo agregar a errores si contiene palabras clave de error
                        contains_error = any(pattern.lower() in text.lower() for pattern in section_team_error_patterns)
                        if contains_error:
                            result["errors"].append(text)
                            result["success"] = True
        except Exception:
            continue
    
    # Buscar por texto específico en toda la página
    for pattern in section_team_error_patterns:
        try:
            xpath = f"//*[contains(text(), '{pattern}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        result["success"] = True
                        if text not in result["errors"]:
                            result["errors"].append(text)
        except Exception:
            continue
    
    return result

def navigate_to_courses(driver):
    """Navegar a la página de cursos"""
    driver.get(TEST_URL)
    time.sleep(3)
    return True

def click_enroll_button(driver):
    """Buscar y hacer clic en el botón/enlace 'Enroll'"""
    time.sleep(5)
    
    # Buscar por enlaces con texto 'Enroll'
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        try:
            if link.is_displayed() and "enroll" in link.text.lower():
                driver.execute_script(SCROLL_SCRIPT, link)
                time.sleep(2)
                link.click()
                time.sleep(8)
                return True
        except Exception:
            continue
    return False

def center_enrollment_table(driver):
    """Verificar página de enrollment y preparar tabla - manteniendo scroll arriba"""
    time.sleep(3)
    if not wait_for_table_ready(driver):
        return False
    
    # Mantener el scroll en la parte superior para ver los mensajes de error
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    return True

def fill_student_data(driver):
    """Ingresar datos del estudiante (con section y team vacíos)"""
    take_screenshot(driver, "CP-RF-0005-D", "antes-llenar-datos")
    
    data_entered = fill_student_data_teammates_mejorado(driver, STUDENT_DATA)
    
    take_screenshot(driver, "CP-RF-0005-D", "despues-llenar-datos-section-team-vacios")
    
    return data_entered

def submit_enrollment(driver, wait):
    """Hacer clic en el botón 'Enroll students'"""
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "btn-enroll")))
        driver.execute_script(SCROLL_SCRIPT, button)
        time.sleep(2)
        button.click()
        
        # Esperar a que aparezcan los resultados del enrollment
        print("⏳ Esperando resultados del enrollment...")
        
        # Mantener el scroll en la parte superior para ver mensajes de error
        driver.execute_script("window.scrollTo(0, 0);")
        
        # Esperar por alguno de los elementos que indican que el proceso terminó
        result_indicators = [
            (By.ID, "results-panel"),
            (By.CSS_SELECTOR, ".enroll-results-panel"),
            (By.CSS_SELECTOR, ".bg-danger"),
            (By.CSS_SELECTOR, ".bg-success"),
            (By.XPATH, "//*[contains(text(), 'failed to be enrolled')]"),
            (By.XPATH, "//*[contains(text(), 'successfully enrolled')]"),
            (By.XPATH, "//*[contains(text(), 'Enrollment Results')]")
        ]
        
        # Intentar esperar por cualquiera de estos indicadores
        for locator in result_indicators:
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))
                print("✅ Resultados del enrollment cargados")
                # Asegurar que el scroll esté arriba para ver mensajes de error
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(3)  # Espera adicional para asegurar que todo se cargue
                return True
            except Exception:
                continue
        
        # Si ningún indicador específico se encuentra, espera un tiempo fijo
        print("⏳ Esperando tiempo fijo para resultados...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(10)
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar enrollment: {e}")
        return False

def verify_and_report_results(driver):
    """Verificar y reportar errores del enrollment para section y team vacíos"""
    result = verify_section_team_errors(driver)
    
    # Mostrar resultados
    if result["errors"]:
        print("Errores encontrados (esperados):")
        for error in result["errors"]:
            print(f"  • {error}")
        print("")
    
    # Resultado final con más información
    if result["success"]:
        print("✅ TEST CP-RF-0005-D: EXITOSO")
        print("   - Errores de validación de Section/Team detectados correctamente")
        print("   - El sistema rechazó correctamente el formulario con campos vacíos")
        return True
    else:
        print("❌ TEST CP-RF-0005-D: FALLIDO")
        print("   - No se detectaron los errores de validación esperados")
        print("   - Mensaje esperado: 'Found empty compulsory fields' o similar")
        
        # Información adicional para debug
        print("\n🔍 Debug - Buscando elementos con errores de campos vacíos:")
        try:
            # Buscar elementos bg-danger
            danger_elements = driver.find_elements(By.CSS_SELECTOR, ".bg-danger")
            for i, element in enumerate(danger_elements):
                if element.is_displayed():
                    text = element.text.strip()
                    print(f"   Elemento bg-danger {i+1}: {text}")
            
            # Buscar en resultados de enrollment
            results_elements = driver.find_elements(By.CSS_SELECTOR, ".enroll-results-panel")
            for i, element in enumerate(results_elements):
                if element.is_displayed():
                    text = element.text.strip()
                    print(f"   Panel de resultados {i+1}: {text[:200]}...")
                    
        except Exception as e:
            print(f"   Error buscando elementos: {e}")
            
        return False

def test_campos_section_team_vacios():
    print("Datos de prueba:")
    for key, value in STUDENT_DATA.items():
        if key in ["section", "team"]:
            print(f"  {key.title()}: [VACÍO] - Caso de prueba")
        else:
            print(f"  {key.title()}: {value}")
    print("")
    
    driver = None
    
    try:
        # Crear WebDriver usando la estructura global
        driver = get_driver_for_rf("0005")
        wait = WebDriverWait(driver, 10)
        
        # Ejecutar pasos del test
        if not navigate_to_courses(driver):
            return False
            
        if not click_enroll_button(driver):
            return False
            
        if not center_enrollment_table(driver):
            return False
            
        if not fill_student_data(driver):
            return False
        
        # Primera captura de pantalla
        take_screenshot(driver, "CP-RF-0005-D", "datos-ingresados-section-team-vacios")
        
        if not submit_enrollment(driver, wait):
            return False
        
        # Segunda captura de pantalla
        take_screenshot(driver, "CP-RF-0005-D", "resultado-error-section-team-vacios")
        
        return verify_and_report_results(driver)
            
    except Exception as e:
        print("\nTEST CP-RF-0005-D: ERROR CRÍTICO")
        print(f"Error: {e}")
        
        # Captura de pantalla del error
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0005-D", "error-critico")
        except Exception:
            pass
            
        return False
        
    finally:
        # Limpiar recursos
        if driver:
            try:
                print("🧹 Cerrando navegador...")
                driver.quit()
            except Exception:
                pass

def main():
    """Función principal para ejecutar el test"""
    print("SUITE DE PRUEBAS RF-0005")
    print("Caso: CP-RF-0005-D - Campos Section y Team vacíos")
    print("=" * 60)
    
    result = test_campos_section_team_vacios()
    
    print("\n" + "=" * 60)
    if result:
        print("RESULTADO FINAL: EXITOSO")
    else:
        print("RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()
