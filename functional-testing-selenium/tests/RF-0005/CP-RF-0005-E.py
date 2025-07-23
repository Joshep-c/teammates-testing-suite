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
    "name": "Ana Lucía",
    "section": "Grupo A", 
    "team": "Equipo 3",
    "email": "ana.lucia@unsa.edu.pe",
    "comments": ""  # Comentarios vacíos - caso de prueba (permitido)
}

# Funciones principales simplificadas
def wait_for_table_ready(driver):
    """Esperar a que la tabla de enrollment esté lista"""
    try:
        wait = WebDriverWait(driver, 15)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        if table.is_displayed():
            time.sleep(3)
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
            
            # Para comments, permitir que esté vacío (caso de prueba)
            if field_name == "comments":
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
                        
                        if field_name != "comments":  # Solo contar campos obligatorios
                            fields_filled += 1
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        
        return fields_filled >= 4  # Todos los campos obligatorios
    except Exception:
        return False

def fill_student_data_teammates_mejorado(driver, student_data):
    """Ingresar datos del estudiante usando Handsontable"""
    if not handle_teammates_enrollment_form(driver):
        return False
    
    return fill_handsontable_data(driver, student_data)

def verify_successful_enrollment_with_empty_comments(driver):
    """Verificar que el enrollment fue exitoso con comentarios vacíos"""
    result = {"success": False, "messages": [], "errors": []}
    
    # Buscar indicadores de éxito
    success_indicators = [
        "successfully enrolled", "student added", "enrollment complete",
        "student has been enrolled", "enrollment successful"
    ]
    success_selectors = [".success", ".alert-success", "*[class*='success']"]
    
    for selector in success_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        result["messages"].append(text)
                        result["success"] = True
        except Exception:
            continue
    
    # Buscar por texto específico
    for indicator in success_indicators:
        try:
            xpath = f"//*[contains(text(), '{indicator}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for element in elements:
                if element.is_displayed():
                    result["success"] = True
        except Exception:
            continue
    
    # Buscar errores (no debería haber)
    error_selectors = [".error", ".alert-danger", "*[class*='error']"]
    for selector in error_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
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
    """Verificar página de enrollment y preparar tabla"""
    time.sleep(3)
    if not wait_for_table_ready(driver):
        return False
    
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    return True

def fill_student_data(driver):
    """Ingresar datos del estudiante (con comentarios vacíos)"""
    take_screenshot(driver, "CP-RF-0005-E", "antes-llenar-datos")
    
    data_entered = fill_student_data_teammates_mejorado(driver, STUDENT_DATA)
    
    take_screenshot(driver, "CP-RF-0005-E", "despues-llenar-datos-comentarios-vacios")
    
    return data_entered

def submit_enrollment(driver, wait):
    """Hacer clic en el botón 'Enroll students' y esperar a que se procese"""
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "btn-enroll")))
        driver.execute_script(SCROLL_SCRIPT, button)
        time.sleep(2)
        button.click()
        
        # Esperar a que aparezcan los resultados del enrollment
        result_found = False
        max_wait = 20  # 20 segundos máximo
        wait_interval = 1
        
        for attempt in range(max_wait):
            time.sleep(wait_interval)
            
            # Buscar indicadores de éxito
            success_selectors = [
                ".alert-success", ".success", ".bg-success",
                "*[class*='success']", ".enroll-results-panel"
            ]
            
            # Buscar indicadores de error o validación
            error_selectors = [
                ".alert-danger", ".error", ".bg-danger", 
                "*[class*='error']", "*[class*='danger']"
            ]
            
            # Verificar éxito
            for selector in success_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.text.strip():
                            print(f"Resultado encontrado (éxito): {element.text.strip()[:100]}")
                            result_found = True
                            break
                except Exception:
                    continue
                if result_found:
                    break
            
            # Verificar errores
            if not result_found:
                for selector in error_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if element.is_displayed() and element.text.strip():
                                print(f"Resultado encontrado (error): {element.text.strip()[:100]}")
                                result_found = True
                                break
                    except Exception:
                        continue
                    if result_found:
                        break
            
            if result_found:
                break
                
            # Imprimir progreso cada 5 segundos
            if attempt % 5 == 4:
                print(f"Esperando resultados del enrollment... ({attempt + 1}/{max_wait}s)")
        
        if not result_found:
            print("Advertencia: No se detectaron resultados del enrollment después de 20s")
        
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error en submit_enrollment: {e}")
        return False

def verify_and_report_results(driver):
    """Verificar y reportar resultados del enrollment con comentarios vacíos"""
    result = verify_successful_enrollment_with_empty_comments(driver)
    
    # Mostrar resultados
    if result["messages"]:
        print("Mensajes de éxito:")
        for msg in result["messages"]:
            print(f"  • {msg}")
    
    if result["errors"]:
        print("Errores encontrados (no esperados):")
        for error in result["errors"]:
            print(f"  • {error}")
    
    # Resultado final
    if result["success"] and not result["errors"]:
        print("\nTEST CP-RF-0005-E: EXITOSO - Inscripción exitosa con comentarios vacíos")
        return True
    else:
        print("\nTEST CP-RF-0005-E: FALLIDO - La inscripción no fue exitosa o se encontraron errores")
        return False

def test_comentarios_en_blanco():
    print("Datos de prueba:")
    for key, value in STUDENT_DATA.items():
        if key == "comments":
            print(f"  {key.title()}: [VACÍO] - Caso de prueba (permitido)")
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
        take_screenshot(driver, "CP-RF-0005-E", "datos-ingresados-comentarios-vacios")
        
        if not submit_enrollment(driver, wait):
            return False
        
        # Segunda captura de pantalla
        take_screenshot(driver, "CP-RF-0005-E", "resultado-exitoso-comentarios-vacios")
        
        return verify_and_report_results(driver)
            
    except Exception as e:
        print("\nTEST CP-RF-0005-E: ERROR CRÍTICO")
        print(f"Error: {e}")
        
        # Captura de pantalla del error
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0005-E", "error-critico")
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
    print("Caso: CP-RF-0005-E - Comentarios en blanco (permitido)")
    print("=" * 60)
    
    result = test_comentarios_en_blanco()
    
    print("\n" + "=" * 60)
    if result:
        print("RESULTADO FINAL: EXITOSO")
    else:
        print("RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()
