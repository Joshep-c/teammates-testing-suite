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
    "name": "",  # Nombre vacío - caso de prueba
    "section": "Grupo A", 
    "team": "Equipo 5",
    "email": "juan.perez@unsa.edu.pe",
    "comments": "Sin nombre"
}

# Funciones principales simplificadas
def wait_for_table_ready(driver):
    """Esperar a que la tabla de enrollment esté lista"""
    try:
        wait = WebDriverWait(driver, 15)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        if table.is_displayed():
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
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
            
            # Para este caso específico, el nombre debe quedar vacío
            if field_name == "name":
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
                        
                        if field_name != "name":  # Solo contar campos que no sean el nombre
                            fields_filled += 1
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        
        return fields_filled >= 3  # Esperamos al menos 3 campos (sin contar el nombre vacío)
    except Exception:
        return False

def fill_student_data_teammates_mejorado(driver, student_data):
    """Ingresar datos del estudiante usando Handsontable"""
    if not handle_teammates_enrollment_form(driver):
        return False
    
    return fill_handsontable_data(driver, student_data)

def verify_student_enrollment_error(driver):
    """Verificar errores específicos del enrollment para nombre vacío"""
    result = {"success": False, "messages": [], "errors": []}
    
    # Buscar errores específicos para campos obligatorios vacíos (como se muestra en tu salida)
    name_error_patterns = [
        "Found empty compulsory fields",
        "empty compulsory fields",
        "Student Name is required",
        "Name is required", 
        "Student name cannot be empty",
        "Name field is mandatory",
        "compulsory fields"
    ]
    
    # Buscar errores en elementos comunes, incluyendo específicamente bg-danger
    error_selectors = [
        ".bg-danger", "div.bg-danger", ".card-body.bg-danger",
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
                        contains_error = any(pattern.lower() in text.lower() for pattern in name_error_patterns)
                        if contains_error:
                            result["errors"].append(text)
                            result["success"] = True
        except Exception:
            continue
    
    # Buscar por texto específico en toda la página
    for pattern in name_error_patterns:
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

def click_enroll_button(driver, wait):
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
    """Verificar página de enrollment y preparar tabla"""
    time.sleep(3)
    if not wait_for_table_ready(driver):
        return False
    
    driver.execute_script("window.scrollTo(0, 200);")
    time.sleep(2)
    return True

def fill_student_data(driver):
    """Ingresar datos del estudiante (con nombre vacío)"""
    take_screenshot(driver, "CP-RF-0005-B", "antes-llenar-datos")
    
    data_entered = fill_student_data_teammates_mejorado(driver, STUDENT_DATA)
    
    take_screenshot(driver, "CP-RF-0005-B", "despues-llenar-datos-nombre-vacio")
    
    return data_entered

def submit_enrollment(driver, wait):
    """Hacer clic en el botón 'Enroll students'"""
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "btn-enroll")))
        driver.execute_script(SCROLL_SCRIPT, button)
        button.click()
        time.sleep(5)
        return True
    except Exception:
        return False

def verify_and_report_results(driver):
    """Verificar y reportar errores del enrollment para nombre vacío"""
    result = verify_student_enrollment_error(driver)
    
    # Mostrar resultados
    if result["errors"]:
        print("Errores encontrados (esperados):")
        for error in result["errors"]:
            print(f"  • {error}")
        print("")
    
    # Resultado final con más información
    if result["success"]:
        print("✅ TEST CP-RF-0005-B: EXITOSO")
        print("   - Error de validación detectado correctamente")
        print("   - El sistema rechazó correctamente el formulario con nombre vacío")
        return True
    else:
        print("❌ TEST CP-RF-0005-B: FALLIDO")
        print("   - No se detectó el error de validación esperado")
        print("   - Mensaje esperado: 'Found empty compulsory fields' o similar")
        
        # Información adicional para debug
        print("\n🔍 Debug - Buscando elementos con clase bg-danger:")
        try:
            danger_elements = driver.find_elements(By.CSS_SELECTOR, ".bg-danger")
            for i, element in enumerate(danger_elements):
                if element.is_displayed():
                    text = element.text.strip()
                    print(f"   Element {i+1}: {text}")
        except Exception as e:
            print(f"   Error buscando elementos: {e}")
            
        return False

def test_nombre_estudiante_vacio():
    print("Datos de prueba:")
    for key, value in STUDENT_DATA.items():
        if key == "name":
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
            
        if not click_enroll_button(driver, wait):
            return False
            
        if not center_enrollment_table(driver):
            return False
            
        if not fill_student_data(driver):
            return False
        
        # Primera captura de pantalla
        take_screenshot(driver, "CP-RF-0005-B", "datos-ingresados-nombre-vacio")
        
        if not submit_enrollment(driver, wait):
            return False
        
        # Segunda captura de pantalla
        take_screenshot(driver, "CP-RF-0005-B", "resultado-error-nombre-vacio")
        
        return verify_and_report_results(driver)
            
    except Exception as e:
        print("\nTEST CP-RF-0005-B: ERROR CRÍTICO")
        print(f"Error: {e}")
        
        # Captura de pantalla del error
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0005-B", "error-critico")
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
    print("Caso: CP-RF-0005-B - Nombre de estudiante vacío")
    print("=" * 60)
    
    result = test_nombre_estudiante_vacio()
    
    print("\n" + "=" * 60)
    if result:
        print("RESULTADO FINAL: EXITOSO")
    else:
        print("RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()
