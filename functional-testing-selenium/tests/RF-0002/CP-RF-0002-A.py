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

def test_campos_vacios():
    """
    CP-RF-0002-A: Campos vacíos
    RF-0002: Partición de equivalencia
    Verificar que el formulario no acepte campos vacíos
    """
    print("=== INICIANDO TEST CP-RF-0002-A ===")
    print("Objetivo: Verificar que el formulario no acepte campos vacíos")
    print("Datos de prueba:")
    print("  Nombre: \"\"")
    print("  Email: \"\"")
    print("  Display: \"\"")
    print("")
    
    try:
        # Crear WebDriver usando la estructura global (maneja Chrome automáticamente)
        driver = get_driver_for_rf("0002")
        wait = WebDriverWait(driver, 10)
        
        # Navegar directamente al curso (las cookies se cargan automáticamente)
        url = "https://modern-vortex-463217-h9.appspot.com/web/instructor/courses/edit?courseid=PS"
        driver.get(url)
        
        # Verificar si estamos autenticados o necesitamos login manual
        time.sleep(3)
        current_url = driver.current_url
        
        if "accounts.google.com" in current_url or "login" in current_url.lower():
            print("⚠ No se detectó sesión guardada. Se requiere autenticación manual.")
            print("1. Completa el login en la ventana del navegador")
            print("2. Navega al curso deseado")
            print("3. El test continuará automáticamente...")
            
            # Esperar hasta que el usuario complete la autenticación
            while "accounts.google.com" in driver.current_url or "login" in driver.current_url.lower():
                time.sleep(2)
        else:
            # Esperar a que la página cargue completamente
            time.sleep(3)
        
        # PASO 1: Desplegar el formulario        # Definir selectores para el botón de desplegar formulario
        button_selectors = [
            (By.ID, "btn-add-instructor"),
            (By.XPATH, "//button[contains(text(), 'Add New Instructor')]"),
            (By.XPATH, "//button[contains(text(), 'Add Instructor')]"),
        ]
        
        # Intentar desplegar el formulario
        if not find_and_click_button(driver, button_selectors):
            print("⚠ No se pudo desplegar el formulario, continuando con elementos disponibles")
        else:
            time.sleep(2)  # Esperar a que se despliegue
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # PASO 2: Localizar campos del formulario        # Verificar que los campos estén disponibles
        required_fields = ["name-instructor-1", "email-instructor-1", "displayed-name-instructor-1"]
        field_status = verify_form_fields(driver, required_fields)
        
        fields_ok = all(status["found"] and status["visible"] for status in field_status.values())
        
        if not fields_ok:
            print("✗ No todos los campos están disponibles:")
            for field_id, status in field_status.items():
                print(f"  - {field_id}: Found={status['found']}, Visible={status['visible']}")
            raise Exception("Campos del formulario no disponibles")        # PASO 3: Asegurar que los campos estén vacíos usando función global
        for field_id in required_fields:
            clear_and_send_keys(driver, field_id, "")  # Enviar cadena vacía

        # Tomar screenshot inicial
        take_screenshot(driver, "CP-RF-0002-A", "entrada")        # PASO 4: Hacer clic en el botón de envío con campos vacíos
        submit_selectors = [
            (By.ID, "btn-save-instructor-1"),
            (By.XPATH, "//button[contains(text(), 'Add Instructor') and contains(@id, 'save')]")
        ]
        
        if find_and_click_button(driver, submit_selectors):            # Esperar respuesta
            time.sleep(3)
            
            # PASO 5: Buscar mensajes de error
            error_messages = find_error_messages(driver)
            success_indicators = find_success_indicators(driver)
            
            # Evaluar resultado
            if error_messages:
                print("✓ Mensajes de error encontrados:")
                for i, msg in enumerate(error_messages, 1):
                    print(f"  Error {i}: '{msg}'")
                resultado = "TEST EXITOSO: Se mostraron mensajes de error para campos vacíos"
            elif success_indicators:
                print("✗ Indicadores de éxito encontrados (inesperado):")
                for i, msg in enumerate(success_indicators, 1):
                    print(f"  Éxito {i}: '{msg}'")
                resultado = "TEST FALLIDO: El formulario se envió exitosamente con campos vacíos"
            else:
                resultado = "TEST INCONCLUSO: No se encontraron mensajes de error ni éxito"
        else:
            resultado = "TEST FALLIDO: No se pudo hacer clic en el botón de envío"
        
        # Tomar screenshot final
        take_screenshot(driver, "CP-RF-0002-A", "salida")
        
        # Resultado del test
        print(f"\n=== RESULTADO: {resultado} ===")
        
        return resultado
        
    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
            if 'driver' in locals():
                driver.quit()
    
    if __name__ == "__main__":
        resultado = test_campos_vacios()
        print(f"\nResultado final: {resultado}")
