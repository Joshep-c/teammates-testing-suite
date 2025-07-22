import subprocess
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'util'))
from driver_setup import get_driver

def close_chrome_processes():
    """Cierra todos los procesos de Chrome para evitar conflictos"""
    try:
        print("Cerrando procesos de Chrome existentes...")
        subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], 
                      capture_output=True, text=True, check=False)
        time.sleep(3)
        print("Procesos de Chrome cerrados.")
        return True
    except Exception as e:
        print(f"Error al cerrar Chrome: {e}")
        return False

def test_email_vacio():
    """
    CP-RF-0002-C: Email vacío, resto válido
    RF-0002: Partición de equivalencia
    Verificar validación de campo Email
    """
    print("=== INICIANDO TEST CP-RF-0002-C ===")
    print("Objetivo: Verificar validación de campo Email")
    print("Datos de prueba:")
    print("  Nombre: \"John Doe\"")
    print("  Email: \"\"")
    print("  Display: \"Instructor\"")
    print("  Access: \"Co-owner\"")
    print("")
    
    # Cerrar Chrome antes de empezar
    close_chrome_processes()
    
    try:
        # Crear WebDriver usando driver_setup
        driver = get_driver()
        wait = WebDriverWait(driver, 10)
        
        # Agregar script para evitar detección de automatización
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
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
            # Tomar screenshot inicial
            screenshot_path = os.path.join(os.path.dirname(__file__), "img", "IMG-1-CP-RF-0002-C.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot inicial guardado: {screenshot_path}")
        
        # Esperar a que la página cargue completamente
        time.sleep(3)
        
        # Buscar y llenar los campos del formulario
        print("Buscando campos del formulario...")
        
        try:
            # Localizar campos usando los IDs reales encontrados
            name_field = wait.until(
                EC.presence_of_element_located((By.ID, "name-instructor-1"))
            )
            email_field = driver.find_element(By.ID, "email-instructor-1")
            display_field = driver.find_element(By.ID, "displayed-name-instructor-1")
            
            print("✓ Todos los campos encontrados")
            
            # Limpiar todos los campos primero
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar campos EXCEPTO el email (dejarlo vacío intencionalmente)
            name_field.send_keys("John Doe")
            print("✓ Campo Nombre llenado: John Doe")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            print("⚠ Campo Email dejado vacío intencionalmente")
            
            # Verificar que el email esté realmente vacío
            email_value = email_field.get_attribute("value")
            if email_value:
                email_field.clear()
                print("✓ Campo Email limpiado para asegurar que esté vacío")
            
            # Hacer clic en "Add Instructor"
            add_instructor_button = driver.find_element(By.ID, "btn-save-instructor-1")
            add_instructor_button.click()
            print("✓ Clic en 'Add Instructor'")
            
            # Esperar a que aparezcan mensajes de error
            time.sleep(3)
            
            # Buscar mensajes de error específicos para campo Email
            error_messages = []
            email_error_found = False
            
            # Buscar errores por diferentes selectores
            error_selectors = [
                (By.CLASS_NAME, "text-danger"),
                (By.CLASS_NAME, "alert-danger"),
                (By.CLASS_NAME, "error"),
                (By.CLASS_NAME, "invalid-feedback"),
                (By.XPATH, "//*[contains(@class, 'error')]"),
                (By.XPATH, "//*[contains(@class, 'invalid')]")
            ]
            
            for selector_type, selector_value in error_selectors:
                try:
                    found_errors = driver.find_elements(selector_type, selector_value)
                    for error in found_errors:
                        if error.is_displayed() and error.text.strip():
                            error_text = error.text.strip()
                            error_messages.append(error_text)
                            
                            # Verificar si el error se refiere al campo email
                            if any(keyword in error_text.lower() for keyword in ['email', 'correo', 'mail', 'e-mail']):
                                email_error_found = True
                except:
                    continue
            
            # Verificar validación HTML5 específica del campo email
            email_validity = False
            if email_field.get_attribute("required"):
                validity = driver.execute_script("return arguments[0].validity.valid", email_field)
                if not validity:
                    email_validity = True
                    print("✓ Validación HTML5 detectada en campo Email")
            
            # Evaluar resultado
            if error_messages:
                print("✓ Mensajes de error encontrados:")
                for i, error in enumerate(error_messages, 1):
                    print(f"  Error {i}: {error}")
                
                if email_error_found:
                    resultado = "TEST EXITOSO: Se mostró mensaje de error específico para campo Email vacío"
                else:
                    resultado = "TEST PARCIAL: Se mostraron errores pero no específicos para el campo Email"
            elif email_validity:
                resultado = "TEST EXITOSO: Validación HTML5 funcionando para campo Email vacío"
            else:
                resultado = "TEST FALLIDO: No se mostró mensaje de error específico para campo Email"
            
        except Exception as e:
            print(f"✗ Error al interactuar con el formulario: {e}")
            resultado = "TEST FALLIDO: Error al interactuar con el formulario"
        
        # Tomar screenshot final
        final_screenshot_path = os.path.join(os.path.dirname(__file__), "img", "IMG-2-CP-RF-0002-C.png")
        driver.save_screenshot(final_screenshot_path)
        print(f"Screenshot final guardado: {final_screenshot_path}")
        
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
        resultado = test_email_vacio()
        print(f"\nResultado final: {resultado}")
