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

def test_multiples_campos_vacios():
    """
    CP-RF-0002-I: Múltiples campos vacíos
    RF-0002: Partición de equivalencia
    Verificar validación con nombre y email vacíos
    """
    print("=== INICIANDO TEST CP-RF-0002-I ===")
    print("Objetivo: Verificar validación con múltiples campos vacíos")
    print("Datos de prueba:")
    print("  Nombre: \"\"")
    print("  Email: \"\"")
    print("  Display: \"Instructor\"")
    print("  Access: \"Co-owner\"")
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
            print("✓ Autenticación completada")
        else:
            print("✓ Sesión detectada, continuando...")
        
        # Tomar screenshot inicial
        screenshot_path = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-I-entrada.png")
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
            
            # Limpiar campos (dejar vacíos)
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar solo el campo display
            print("✓ Campo Nombre dejado vacío")
            print("✓ Campo Email dejado vacío")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-I-campos-llenados.png")
            driver.save_screenshot(screenshot_path_2)
            print(f"Screenshot después de llenar campos: {screenshot_path_2}")
            
            # Buscar y hacer clic en el botón de envío/guardar
            print("Buscando botón para enviar formulario...")
            
            submit_button = None
            button_selectors = [
                "//button[contains(text(), 'Add')]",
                "//button[contains(text(), 'Save')]", 
                "//button[contains(text(), 'Submit')]",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            for selector in button_selectors:
                try:
                    submit_button = driver.find_element(By.XPATH, selector)
                    if submit_button.is_displayed() and submit_button.is_enabled():
                        print(f"✓ Botón encontrado: {submit_button.text}")
                        break
                except Exception:
                    continue
            
            if not submit_button:
                print("⚠ No se encontró botón de envío, buscando elementos interactivos...")
                # Tomar screenshot para análisis manual
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-I-debug.png")
                driver.save_screenshot(screenshot_path_3)
                print(f"Screenshot para debug: {screenshot_path_3}")
                
                # Intentar encontrar cualquier botón visible
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in all_buttons:
                    if btn.is_displayed():
                        print(f"Botón disponible: '{btn.text}' - ID: {btn.get_attribute('id')}")
                        if "add" in btn.text.lower() or "save" in btn.text.lower():
                            submit_button = btn
                            break
            
            if submit_button:
                # Hacer clic en el botón
                driver.execute_script("arguments[0].click();", submit_button)
                print("✓ Botón clickeado")
                
                # Esperar respuesta del formulario
                time.sleep(3)
                
                # Verificar múltiples mensajes de error
                print("Verificando mensajes de validación...")
                
                errors_found = []
                error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//span[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert')]",
                    "//div[contains(text(), 'required')]",
                    "//div[contains(text(), 'empty')]",
                    "//div[contains(text(), 'name')]",
                    "//div[contains(text(), 'email')]"
                ]
                
                for selector in error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text and error_text not in errors_found:
                                    print(f"✓ Mensaje de error encontrado: {error_text}")
                                    errors_found.append(error_text)
                    except Exception:
                        continue
                
                # Verificar si los campos tienen indicadores de error
                try:
                    name_field_class = name_field.get_attribute("class")
                    if "error" in name_field_class or "invalid" in name_field_class:
                        print("✓ Campo nombre marcado con clase de error")
                        errors_found.append("name_field_error")
                except Exception:
                    pass
                
                try:
                    email_field_class = email_field.get_attribute("class")
                    if "error" in email_field_class or "invalid" in email_field_class:
                        print("✓ Campo email marcado con clase de error")
                        errors_found.append("email_field_error")
                except Exception:
                    pass
                
                # Tomar screenshot final
                screenshot_path_final = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-I-salida.png")
                driver.save_screenshot(screenshot_path_final)
                print(f"Screenshot final: {screenshot_path_final}")
                
                if len(errors_found) >= 2:
                    print("✅ TEST EXITOSO: Se detectaron múltiples validaciones de campos vacíos")
                    print(f"Total de errores encontrados: {len(errors_found)}")
                elif len(errors_found) == 1:
                    print("⚠ TEST PARCIAL: Se detectó una validación, pero se esperaban múltiples")
                    print("Se esperaban errores tanto para nombre como para email")
                else:
                    print("❌ TEST FALLIDO: No se detectaron validaciones de campos vacíos")
                    print("El sistema debería rechazar formularios con campos requeridos vacíos")
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-I-error.png")
            driver.save_screenshot(screenshot_path_error)
            print(f"Screenshot de error: {screenshot_path_error}")
        
    except Exception as e:
        print(f"❌ Error general en el test: {e}")
        
    finally:
        try:
            driver.quit()
            print("✓ Driver cerrado correctamente")
        except Exception:
            pass
        
        print("=== TEST CP-RF-0002-I COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_multiples_campos_vacios()
