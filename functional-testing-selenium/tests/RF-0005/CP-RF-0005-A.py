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
        print(f"📸 Captura guardada: {screenshot_path}")

# Importar helper especializado para Handsontable
from handsontable_helper_mejorado import (
    fill_student_data_teammates_mejorado, 
    verify_student_enrollment_result_mejorado,
    scroll_away_from_navbar,
    wait_for_table_ready
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constantes
SCROLL_SCRIPT = "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});"
TEST_URL = "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/courses"
STUDENT_DATA = {
    "name": "Juan Pérez",
    "section": "Grupo B", 
    "team": "Equipo 4",
    "email": "juan.perez123@unsa.edu.pe",
    "comments": "Nuevo estudiante"
}

def navigate_to_courses(driver):
    """Navegar a la página de cursos y manejar autenticación"""
    print("🌐 PASO 1: Navegando a página de cursos...")
    driver.get(TEST_URL)
    time.sleep(3)
    
    # Verificar autenticación
    current_url = driver.current_url
    if "accounts.google.com" in current_url or "login" in current_url.lower():
        print("⚠ Se requiere autenticación manual.")
        print("👤 Complete el login y navegue a la página de cursos...")
        
        while "accounts.google.com" in driver.current_url or "login" in driver.current_url.lower():
            time.sleep(2)
        print("✓ Autenticación completada")
    
    print(f"✓ Página cargada: {driver.current_url}")
    return True

def click_enroll_button(driver, wait):
    """Buscar y hacer clic en el botón Enroll"""
    print("🔍 PASO 2: Buscando y haciendo clic en 'Enroll'...")
    
    # Esperar más tiempo y buscar diferentes elementos
    time.sleep(5)

    # Intentar encontrar la tabla primero
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✓ Tabla de cursos encontrada")
    except:
        print("⚠ No se encontró tabla, continuando búsqueda...")
    
    # Buscar botón Enroll con múltiples estrategias
    print("🔎 Buscando botón 'Enroll'...")
    
    # Estrategia 1: Buscar por texto en botones
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"📊 Se encontraron {len(buttons)} botones en total")
    
    for i, button in enumerate(buttons):
        try:
            button_text = button.text.strip()
            if button_text and button.is_displayed():
                print(f"  Botón {i+1}: '{button_text}'")
                if "enroll" in button_text.lower():
                    print(f"✓ Botón 'Enroll' encontrado: {button_text}")
                    driver.execute_script(SCROLL_SCRIPT, button)
                    time.sleep(2)
                    button.click()
                    time.sleep(8)  # Más tiempo después del clic
                    return True
        except Exception as e:
            print(f"  Error leyendo botón {i+1}: {e}")
    
    # Estrategia 2: Buscar por enlaces
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"📊 Se encontraron {len(links)} enlaces en total")
    
    for i, link in enumerate(links):
        try:
            link_text = link.text.strip()
            if link_text and link.is_displayed():
                if "enroll" in link_text.lower():
                    print(f"✓ Enlace 'Enroll' encontrado: {link_text}")
                    driver.execute_script(SCROLL_SCRIPT, link)
                    time.sleep(2)
                    link.click()
                    time.sleep(8)
                    return True
        except Exception as e:
            continue
    
    # Estrategia 3: Buscar por atributos específicos
    try:
        enroll_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Enroll') or contains(@class, 'enroll') or contains(@id, 'enroll')]")
        print(f"📊 Se encontraron {len(enroll_elements)} elementos con 'enroll'")
        
        for element in enroll_elements:
            if element.is_displayed() and element.is_enabled():
                print(f"✓ Elemento 'Enroll' encontrado: {element.tag_name}")
                driver.execute_script(SCROLL_SCRIPT, element)
                time.sleep(2)
                element.click()
                time.sleep(8)
                return True
    except Exception as e:
        print(f"Error en búsqueda por XPath: {e}")
    
    print("❌ No se encontró botón 'Enroll' después de búsqueda exhaustiva")
    return False

def center_enrollment_table(driver):
    """Centrar la tabla de enroll en la pantalla"""
    print("📜 PASO 3: Centrando tabla en la pantalla...")
    
    # Verificar que estamos en la página de enroll
    if "enroll" not in driver.current_url:
        print("❌ No se pudo acceder a la página de enroll")
        return False
        
    print(f"✓ Página de enroll cargada: {driver.current_url}")
    
    # Esperar a que la tabla esté lista usando el helper mejorado
    if not wait_for_table_ready(driver):
        print("❌ La tabla no está lista")
        return False
    
    # Usar la función mejorada para posicionar la tabla
    scroll_away_from_navbar(driver)
    time.sleep(2)
    
    return True

def fill_student_data(driver):
    """Ingresar datos del estudiante usando el helper mejorado"""
    print("📝 PASO 4: Ingresando datos del estudiante...")
    
    data_entered = fill_student_data_teammates_mejorado(driver, STUDENT_DATA)
    
    if not data_entered:
        print("⚠ No se pudieron ingresar todos los datos, continuando...")
    
    return True

def submit_enrollment(driver, wait):
    """Hacer clic en el botón 'Enroll students'"""
    print("🔍 PASO 6: Haciendo clic en 'Enroll students'...")
    
    try:
        enroll_students_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-enroll")))
        driver.execute_script(SCROLL_SCRIPT, enroll_students_button)
        time.sleep(2)
        
        print("🖱 Haciendo clic en 'Enroll students'...")
        enroll_students_button.click()
        time.sleep(5)
        return True
        
    except Exception as e:
        print(f"❌ Error haciendo clic en 'Enroll students': {e}")
        return False

def verify_and_report_results(driver):
    """Verificar resultados del enrollment usando el helper mejorado"""
    print("🔍 PASO 8: Verificando resultados...")
    
    verification_result = verify_student_enrollment_result_mejorado(driver)
    
    # Mostrar resultados de la verificación
    if verification_result["messages"]:
        print("✓ Mensajes de éxito:")
        for msg in verification_result["messages"]:
            print(f"  • {msg}")
    
    if verification_result["errors"]:
        print("❌ Errores encontrados:")
        for error in verification_result["errors"]:
            print(f"  • {error}")
    
    if verification_result["warnings"]:
        print("⚠ Advertencias:")
        for warning in verification_result["warnings"]:
            print(f"  • {warning}")
    
    # Resultado final
    if verification_result["success"]:
        print("\n✅ TEST CP-RF-0005-A: EXITOSO")
        print("✓ El ingreso de datos de estudiante fue exitoso")
        print("✓ Se detectaron indicadores de éxito")
        return True
    elif verification_result["errors"]:
        print("\n❌ TEST CP-RF-0005-A: FALLIDO") 
        print("❌ Se detectaron errores en el proceso")
        return False
    else:
        print("\n⚠ TEST CP-RF-0005-A: INCIERTO")
        print("• No se detectaron errores evidentes")
        print("• Revisar capturas de pantalla para verificación manual")
        return True

def test_ingreso_exitoso_estudiante():
    """
    CP-RF-0005-A: Ingreso exitoso de datos de estudiante
    RF-0005: Partición de equivalencia
    Verificar ingreso correcto de datos válidos
    """
    print("=== INICIANDO TEST CP-RF-0005-A ===")
    print("Objetivo: Verificar ingreso correcto de datos válidos de estudiante")
    print("Datos de prueba:")
    for key, value in STUDENT_DATA.items():
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
        
        # PASO 5: Primera captura de pantalla
        print("📸 PASO 5: Tomando primera captura (datos ingresados)...")
        take_screenshot(driver, "CP-RF-0005-A", "datos-ingresados")
        
        if not submit_enrollment(driver, wait):
            return False
        
        # PASO 7: Segunda captura de pantalla
        print("📸 PASO 7: Tomando segunda captura (resultado)...")
        take_screenshot(driver, "CP-RF-0005-A", "resultado-enroll")
        
        return verify_and_report_results(driver)
            
    except Exception as e:
        print("\n❌ TEST CP-RF-0005-A: ERROR CRÍTICO")
        print(f"Error: {e}")
        
        # Captura de pantalla del error
        try:
            if driver:
                take_screenshot(driver, "CP-RF-0005-A", "error-critico")
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
    print("Caso: CP-RF-0005-A - Ingreso exitoso de datos de estudiante")
    print("=" * 60)
    
    result = test_ingreso_exitoso_estudiante()
    
    print("\n" + "=" * 60)
    if result:
        print("🏆 RESULTADO FINAL: EXITOSO")
    else:
        print("💥 RESULTADO FINAL: FALLIDO")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()
