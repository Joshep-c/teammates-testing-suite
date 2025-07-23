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

# Primer estudiante - datos únicos para inscripción exitosa
FIRST_STUDENT_DATA = {
    "name": "Carlos Eduardo Morales",
    "section": "Sección B", 
    "team": "Equipo Beta",
    "email": "carlos.morales.unique@unsa.edu.pe",  # Email único
    "comments": "Primer estudiante - inscripción inicial exitosa"
}

# Segundo estudiante - mismo email que el primero para generar duplicado
SECOND_STUDENT_DATA = {
    "name": "Ana Patricia Silva",
    "section": "Sección C", 
    "team": "Equipo Gamma",
    "email": "carlos.morales.unique@unsa.edu.pe",  # Mismo email = duplicado
    "comments": "Segundo estudiante - email duplicado para prueba"
}

def wait_for_table_ready(driver):
    """Esperar a que la tabla de enrollment esté lista"""
    try:
        wait = WebDriverWait(driver, 15)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
        if table.is_displayed():
            time.sleep(3)
            return True
    except Exception:
        time.sleep(5)
    return True

def scroll_to_table(driver):
    """Scroll hacia la tabla de enrollment"""
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

def scroll_to_button(driver):
    """Scroll hacia abajo para ver el botón Enroll students y asegurar que esté accesible"""
    try:
        # Buscar el botón primero
        button = driver.find_element(By.ID, "btn-enroll")
        # Scroll hacia el botón con margen adicional para evitar interceptación
        driver.execute_script("""
            var button = arguments[0];
            var rect = button.getBoundingClientRect();
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            var targetY = rect.top + scrollTop - 200; // 200px de margen superior
            window.scrollTo(0, targetY);
        """, button)
        time.sleep(2)
        print("Scroll hacia el botón 'Enroll students' completado")
    except Exception as e:
        # Fallback: scroll hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 300);")
        time.sleep(2)
        print(f"Fallback scroll ejecutado: {e}")

def handle_teammates_enrollment_form(driver):
    """Verificar que la tabla de Handsontable esté lista"""
    try:
        gridcells = driver.find_elements(By.CSS_SELECTOR, 'td[role="gridcell"]')
        return len(gridcells) > 0
    except Exception:
        return False

def fill_handsontable_data(driver, student_data, row_number=1):
    """Llenar datos en tabla Handsontable de TEAMMATES en una fila específica"""
    try:
        gridcells = driver.find_elements(By.CSS_SELECTOR, 'td[role="gridcell"]')
        if not gridcells:
            return False
        
        field_to_column = {
            "section": 1, "team": 2, "name": 3, "email": 4, "comments": 5
        }
        
        table_container = driver.find_element(By.XPATH, "//table[.//td[@role='gridcell']]")
        fields_filled = 0
        
        for field_name, column_index in field_to_column.items():
            value = student_data.get(field_name, "")
            if not value and field_name != "comments":
                continue
            
            # XPath para fila específica
            xpath_options = [
                f".//tbody/tr[{row_number}]/td[{column_index}][@role='gridcell']",
                f".//tr[{row_number}]/td[{column_index}][@role='gridcell']",
                f"(.//td[@role='gridcell'])[{(row_number - 1) * 5 + column_index}]"
            ]
            
            for xpath in xpath_options:
                try:
                    cell = table_container.find_element(By.XPATH, xpath)
                    if cell.is_displayed():
                        # No hacer scroll a las celdas para evitar interferencias
                        time.sleep(0.5)
                        
                        actions = ActionChains(driver)
                        actions.double_click(cell).perform()
                        time.sleep(1)
                        
                        try:
                            edit_input = driver.find_element(By.CSS_SELECTOR, "input.handsontableInput")
                            edit_input.clear()
                            edit_input.send_keys(value)
                            edit_input.send_keys(Keys.ENTER)
                        except Exception:
                            actions.send_keys(value).perform()
                            actions.send_keys(Keys.ENTER).perform()
                        
                        fields_filled += 1
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        
        return fields_filled >= 4
    except Exception:
        return False

def fill_student_data_teammates_mejorado(driver, student_data, row_number=1):
    """Ingresar datos del estudiante usando Handsontable en una fila específica"""
    if not handle_teammates_enrollment_form(driver):
        return False
    
    return fill_handsontable_data(driver, student_data, row_number)

def fill_both_students_data(driver):
    """Ingresar datos de ambos estudiantes en la misma tabla (filas 1 y 2)"""
    print("Llenando datos de ambos estudiantes...")
    take_screenshot(driver, "CP-RF-0005-J", "01-antes-llenar-datos")
    
    # Llenar primer estudiante en fila 1
    print("Llenando primer estudiante en fila 1...")
    first_student_success = fill_student_data_teammates_mejorado(driver, FIRST_STUDENT_DATA, row_number=1)
    
    if not first_student_success:
        print("Error al llenar datos del primer estudiante")
        return False
    
    time.sleep(1)
    take_screenshot(driver, "CP-RF-0005-J", "02-primer-estudiante-llenado")
    
    # Llenar segundo estudiante en fila 2 (email duplicado)
    print("Llenando segundo estudiante en fila 2 con email duplicado...")
    second_student_success = fill_student_data_teammates_mejorado(driver, SECOND_STUDENT_DATA, row_number=2)
    
    if not second_student_success:
        print("Error al llenar datos del segundo estudiante")
        return False
    
    take_screenshot(driver, "CP-RF-0005-J", "03-ambos-estudiantes-llenados")
    print("Ambos estudiantes ingresados exitosamente")
    
    return True

def verify_duplicate_email_error(driver):
    """Verificar errores específicos para email duplicado"""
    result = {"success": False, "messages": [], "errors": []}
    
    # Patrones de error específicos para email duplicado en TEAMMATES
    duplicate_email_error_patterns = [
        "Found duplicated emails",  # Patrón exacto encontrado en TEAMMATES
        "E-mail Address already in use for another student in this course",
        "Email already exists",
        "Email address already in use",
        "Duplicate email address",
        "Email already registered",
        "This email is already used by another student",
        "Email address is not unique",
        "already in use",
        "duplicated emails"  # Variante del patrón principal
    ]
    
    # Selectores para buscar errores (incluyendo el selector específico encontrado)
    error_selectors = [
        ".bg-danger", ".card-body.bg-danger", ".alert-danger", ".error", 
        "*[class*='error']", ".invalid-feedback", ".text-danger", 
        "*[class*='invalid']", "td", ".enroll-results-panel",
        ".card-body.bg-danger.text-white",  # Selector específico para "Found duplicated emails"
        "[class*='bg-danger']"  # Alternativo para capturar variantes
    ]
    
    # Buscar en elementos con selectors CSS
    for selector in error_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        result["errors"].append(text)
                        # Verificar si contiene algún patrón de error de email duplicado
                        for pattern in duplicate_email_error_patterns:
                            if pattern.lower() in text.lower():
                                result["success"] = True
        except Exception:
            continue
    
    # Buscar por texto específico usando XPath
    for pattern in duplicate_email_error_patterns:
        try:
            xpath = f"//*[contains(text(), '{pattern}')]"
            elements = driver.find_elements(By.XPATH, xpath)
            for element in elements:
                if element.is_displayed():
                    result["success"] = True
                    element_text = element.text.strip()
                    if element_text and element_text not in result["errors"]:
                        result["errors"].append(element_text)
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
    
    scroll_to_table(driver)
    time.sleep(2)
    return True




def submit_enrollment(driver, wait):
    """Hacer clic en el botón 'Enroll students' y esperar a que se procese"""
    try:
        # Buscar el botón sin hacer scroll automático (mantener vista en tabla)
        button = wait.until(EC.presence_of_element_located((By.ID, "btn-enroll")))
        
        # Hacer clic usando JavaScript para evitar interceptación (sin scroll)
        driver.execute_script("arguments[0].click();", button)
        print("Botón 'Enroll students' clickeado exitosamente")
        time.sleep(2)
        
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
            
            # Buscar indicadores de error o validación (especialmente email duplicado)
            error_selectors = [
                ".bg-danger", ".card-body.bg-danger", ".alert-danger", 
                ".error", "*[class*='error']", "*[class*='danger']"
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
            
            # Verificar errores (especialmente email duplicado)
            if not result_found:
                for selector in error_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if element.is_displayed() and element.text.strip():
                                text = element.text.strip()
                                print(f"Resultado encontrado (error): {text[:100]}")
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
        
        return True
    except Exception as e:
        print(f"Error en submit_enrollment: {e}")
        return False

def verify_and_report_results(driver):
    """Verificar y reportar errores del enrollment para email duplicado"""
    result = verify_duplicate_email_error(driver)
    
    if result["errors"]:
        print("Errores encontrados (esperados por email duplicado)")
    
    if result["success"]:
        print("\nTEST CP-RF-0005-J: EXITOSO - Error de email duplicado detectado correctamente")
        print("TEAMMATES detectó correctamente: 'Found duplicated emails'")
        return True
    else:
        print("\nTEST CP-RF-0005-J: FALLIDO - No se detectó el error de email duplicado esperado")
        print("NOTA: Este test verifica detección de emails duplicados en batch enrollment")
        print("ESPERADO: Mensaje 'Found duplicated emails' en elemento bg-danger")
        return False

def test_correo_duplicado():
    print("FLUJO DE PRUEBA - EMAIL DUPLICADO:")
    print("1. Inscripción de ambos estudiantes simultáneamente")
    print("2. Detección de error por email duplicado en el batch")
    print("")
    
    print("Primer estudiante (exitoso):")
    for key, value in FIRST_STUDENT_DATA.items():
        print(f"  {key.title()}: {value}")
    print("")
    
    print("Segundo estudiante (email duplicado):")
    for key, value in SECOND_STUDENT_DATA.items():
        if key == "email":
            print(f"  {key.title()}: {value} - [EMAIL DUPLICADO]")
        else:
            print(f"  {key.title()}: {value}")
    print("")
    
    driver = None
    
    try:
        driver = get_driver_for_rf("0005")
        wait = WebDriverWait(driver, 15)
        
        # FASE 1: Navegación inicial
        if not navigate_to_courses(driver):
            return False
            
        if not click_enroll_button(driver):
            return False
            
        if not center_enrollment_table(driver):
            return False
        
        # FASE 2: Llenar ambos estudiantes en batch       
        if not fill_both_students_data(driver):
            return False
        
        # FASE 3: Submit único para detectar duplicado
        
        # Mantener la vista en la tabla, no hacer scroll hacia el botón
        # El botón debe ser accesible sin scroll adicional
        
        # Submit batch (debería detectar email duplicado)
        if not submit_enrollment(driver, wait):
            return False
        
        # Captura final con error
        take_screenshot(driver, "CP-RF-0005-J", "04-error-email-duplicado-final")
        
        # Verificar error de email duplicado
        return verify_and_report_results(driver)
            
    except Exception as e:
        print(f"\nTEST CP-RF-0005-J: ERROR CRÍTICO - {e}")
        
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0005-J", "error-critico")
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
    """Función principal para ejecutar el test"""
    print("SUITE DE PRUEBAS RF-0005")
    print("Caso: CP-RF-0005-J - Correo duplicado")
    print("=" * 60)
    
    result = test_correo_duplicado()
    
    print("\n" + "=" * 60)
    if result:
        print("RESULTADO FINAL: EXITOSO")
    else:
        print("RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()
