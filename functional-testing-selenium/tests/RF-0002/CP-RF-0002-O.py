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

def test_boundary_analysis_99_chars():
    """
    CP-RF-0002-O: Análisis de límites - 99 caracteres en nombre
    RF-0002: Tabla de decisiones
    Verificar envío exitoso con nombre de 99 caracteres (justo bajo el límite)
    """
    print("=== INICIANDO TEST CP-RF-0002-O ===")
    print("Objetivo: Verificar envío exitoso con nombre de 99 caracteres")
    print("Datos de prueba:")
    
    # Crear nombre de exactamente 99 caracteres
    name_99_chars = "A" * 99
    print(f"  Nombre: \"{name_99_chars}\" (99 caracteres)")
    print(f"  Longitud del nombre: {len(name_99_chars)} caracteres")
    print("  Email: \"boundary.test@example.com\"")
    print("  Display: \"Boundary Test\"")
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
        take_screenshot(driver, "CP-RF-0002-O", "entrada")
        
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
            
            # Limpiar campos
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar campos con datos de prueba
            name_field.send_keys(name_99_chars)
            print(f"✓ Campo Nombre llenado con {len(name_99_chars)} caracteres")
            
            # Verificar que se aceptó todo el texto
            actual_name_value = name_field.get_attribute("value")
            actual_length = len(actual_name_value)
            print(f"   Longitud real en el campo: {actual_length} caracteres")
            
            if actual_length == 99:
                print("✓ EXCELENTE: Se aceptaron todos los 99 caracteres")
            elif actual_length < 99:
                print(f"⚠ TRUNCADO: Solo se aceptaron {actual_length} de 99 caracteres")
            else:
                print(f"⚠ INESPERADO: Se aceptaron {actual_length} caracteres (más de 99)")
            
            email_field.send_keys("boundary.test@example.com")
            print("✓ Campo Email llenado: boundary.test@example.com")
            
            display_field.send_keys("Boundary Test")
            print("✓ Campo Display llenado: Boundary Test")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-O-campos-llenados.png")
            os.makedirs(os.path.dirname(screenshot_path_2), exist_ok=True)
            driver.save_screenshot(screenshot_path_2)
            print(f"Screenshot después de llenar campos: {screenshot_path_2}")
            
            # Buscar y hacer clic en el botón de envío/guardar
            print("Buscando botón para enviar formulario...")
            
            submit_button = None
            button_selectors = [
                "//button[contains(text(), 'Add Instructor')]",
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-O-debug.png")
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
                
                # Verificar si hubo errores o si fue exitoso
                print("Verificando resultado del envío...")
                
                # Verificar mensajes de error
                errors_found = []
                error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//span[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert-danger')]",
                    "//div[contains(text(), 'length')]",
                    "//div[contains(text(), 'limit')]",
                    "//div[contains(text(), 'character')]"
                ]
                
                for selector in error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text and error_text not in errors_found:
                                    print(f"⚠ Mensaje de error encontrado: {error_text}")
                                    errors_found.append(error_text)
                    except Exception:
                        continue
                
                # Verificar indicadores de éxito
                success_indicators = []
                success_selectors = [
                    "//div[contains(@class, 'alert-success')]",
                    "//div[contains(@class, 'success')]",
                    "//div[contains(text(), 'added')]",
                    "//div[contains(text(), 'saved')]",
                    "//div[contains(text(), 'successful')]",
                    "//div[contains(text(), 'created')]"
                ]
                
                for selector in success_selectors:
                    try:
                        success_elements = driver.find_elements(By.XPATH, selector)
                        for element in success_elements:
                            if element.is_displayed():
                                success_text = element.text.strip()
                                if success_text and success_text not in success_indicators:
                                    print(f"✓ Mensaje de éxito encontrado: {success_text}")
                                    success_indicators.append(success_text)
                    except Exception:
                        continue
                
                # Verificar si la URL cambió (indicador de éxito)
                new_url = driver.current_url
                url_changed = new_url != url
                
                # Tomar screenshot final
                take_screenshot(driver, "CP-RF-0002-O", "salida")
                
                # Evaluar resultados
                if len(success_indicators) > 0:
                    print("✅ TEST EXITOSO: Nombre de 99 caracteres aceptado exitosamente")
                    print("El límite es mayor a 99 caracteres o exactamente 100")
                    for msg in success_indicators:
                        print(f"   • {msg}")
                elif url_changed:
                    print("✅ TEST EXITOSO: URL cambió, indicando envío exitoso")
                    print("El nombre de 99 caracteres está dentro del límite permitido")
                elif len(errors_found) == 0:
                    print("✅ TEST EXITOSO: No se detectaron errores de longitud")
                    print("99 caracteres está dentro del límite aceptable")
                else:
                    print("❌ TEST INESPERADO: Se encontraron errores con 99 caracteres")
                    print("99 caracteres debería estar dentro del límite")
                    for error in errors_found:
                        print(f"   • {error}")
                        
                # Análisis adicional del límite
                if actual_length < 99:
                    print(f"\n📊 ANÁLISIS DE LÍMITE:")
                    print(f"   • Campo truncó a {actual_length} caracteres")
                    print(f"   • Límite real del campo: {actual_length} caracteres")
                else:
                    print(f"\n📊 ANÁLISIS DE LÍMITE:")
                    print(f"   • Campo acepta al menos 99 caracteres")
                    print(f"   • Límite es >= 99 caracteres")
                        
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-O-error.png")
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
        
        print("=== TEST CP-RF-0002-O COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_boundary_analysis_99_chars()
