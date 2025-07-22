import sys
import os
import time

# Agregar el path para usar la estructura global util
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'util'))
from driver_setup import get_driver_for_rf
from common_helpers import (take_screenshot, find_and_click_button, find_error_messages, 
                           find_success_indicators, verify_form_fields, clear_and_send_keys)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_registro_instructor():
    """
    CP-RF-0001-A: Registro exitoso de un solo instructor
    RF-0001: Partición de equivalencia
    Verificar que se pueda registrar correctamente un instructor con datos válidos
    """
    print("=== INICIANDO TEST CP-RF-0001-A ===")
    print("Objetivo: Registro exitoso de un solo instructor")
    print("Datos de prueba:")
    print("  Name: Ana Pérez")
    print("  Email: ana@unsa.edu.pe")
    print("  Institution: UNSA")
    print("")
    
    try:
        # Crear WebDriver usando la estructura global (maneja Chrome automáticamente)
        driver = get_driver_for_rf("0001")
        wait = WebDriverWait(driver, 10)
        
        # Navegar directamente a la página de administrador
        admin_url = "https://modern-vortex-463217-h9.appspot.com/web/admin/home"
        driver.get(admin_url)
        
        
        # Verificar que estamos en la página correcta
        if "TEAMMATES" not in driver.title:
            print("ERROR: No se pudo acceder a la página de administrador")
            print("La sesión puede haber expirado.")
            return False
        
        
        # Esperar a que la página cargue completamente
        time.sleep(5)
        
        # Buscar el formulario de registro de instructor        # Verificar que los campos estén disponibles usando función global
        required_fields = ["instructor-name", "instructor-email", "instructor-institution"]
        field_status = verify_form_fields(driver, required_fields)
        
        fields_ok = all(status["found"] and status["visible"] for status in field_status.values())
        
        if not fields_ok:
            print("✗ No todos los campos están disponibles:")
            for field_id, status in field_status.items():
                print(f"  - {field_id}: Found={status['found']}, Visible={status['visible']}")
            take_screenshot(driver, "CP-RF-0001-A", "error-fields")
            raise Exception("Campos del formulario no disponibles")        # Llenar campos usando funciones globales
        clear_and_send_keys(driver, "instructor-name", "Ana Pérez")
        print("✓ Campo 'Name' llenado: Ana Pérez")
        
        clear_and_send_keys(driver, "instructor-email", "ana@unsa.edu.pe")
        print("✓ Campo 'Email' llenado: ana@unsa.edu.pe")
        
        clear_and_send_keys(driver, "instructor-institution", "UNSA")
        print("✓ Campo 'Institution' llenado: UNSA")
        
        # Buscar el botón "Add Instructor" usando función global
        add_button_selectors = [
            (By.ID, "add-instructor"),
            (By.XPATH, "//button[contains(text(), 'Add Instructor')]"),
            (By.XPATH, "//input[@type='submit' and @value='Add Instructor']")
        ]
        
        # Tomar screenshot inicial
        take_screenshot(driver, "CP-RF-0001-A", "entrada")
        
        # Hacer clic en "Add Instructor"
        if find_and_click_button(driver, add_button_selectors):
            
            # Esperar respuesta
            time.sleep(3)
            
            # Desplazar al final de la página para ver resultados
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Buscar indicadores de éxito o error
            success_indicators = find_success_indicators(driver)
            error_messages = find_error_messages(driver)
            
            # Evaluar resultado
            if success_indicators:
                print("✓ Indicadores de éxito encontrados:")
                for i, msg in enumerate(success_indicators, 1):
                    print(f"  Éxito {i}: '{msg}'")
                resultado = "TEST EXITOSO: Instructor registrado correctamente"
            elif error_messages:
                print("✗ Mensajes de error encontrados:")
                for i, msg in enumerate(error_messages, 1):
                    print(f"  Error {i}: '{msg}'")
                resultado = "TEST FALLIDO: Se encontraron errores al registrar instructor"
            else:
                resultado = "TEST INCONCLUSO: No se encontraron indicadores claros de éxito o error"
        else:
            resultado = "TEST FALLIDO: No se pudo hacer clic en el botón 'Add Instructor'"
        
        # Tomar screenshot final
        take_screenshot(driver, "CP-RF-0001-A", "salida")
        
        print(f"\n=== RESULTADO: {resultado} ===")
        return resultado
        
    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-A", "error")
            print("Screenshot de error guardado")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()
if __name__ == "__main__":
    resultado = test_registro_instructor()
    print(f"\nResultado final: {resultado}")