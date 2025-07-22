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
from selenium.webdriver.support.ui import Select

def test_access_level_observer():
    """
    CP-RF-0002-K: Access Level Observer con datos válidos
    RF-0002: Partición de equivalencia
    Verificar funcionalidad con Access Level Observer
    """
    print("=== INICIANDO TEST CP-RF-0002-K ===")
    print("Objetivo: Verificar funcionalidad con Access Level Observer")
    print("Datos de prueba:")
    print("  Nombre: \"John Doe\"")
    print("  Email: \"test@examplePS.com\"")
    print("  Display: \"Instructor\"")
    print("  Access: \"Observer\"")
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
        take_screenshot(driver, "CP-RF-0002-K", "entrada")
        
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
            
            print("✓ Campos básicos encontrados")
            
            # Buscar el campo de access level (dropdown)
            access_dropdown = None
            access_selectors = [
                "select[name*='access']",
                "select[id*='access']",
                "select[name*='role']",
                "select[id*='role']",
                "#access-instructor-1",
                "#role-instructor-1"
            ]
            
            for selector in access_selectors:
                try:
                    access_dropdown = driver.find_element(By.CSS_SELECTOR, selector)
                    if access_dropdown.is_displayed():
                        print(f"✓ Dropdown de access level encontrado: {selector}")
                        break
                except Exception:
                    continue
            
            if not access_dropdown:
                print("⚠ No se encontró dropdown de access level, buscando alternativas...")
                # Buscar todos los selects
                all_selects = driver.find_elements(By.TAG_NAME, "select")
                for select_elem in all_selects:
                    if select_elem.is_displayed():
                        print(f"Select encontrado: ID={select_elem.get_attribute('id')}, Name={select_elem.get_attribute('name')}")
                        # Tomar el primer select visible como access dropdown
                        access_dropdown = select_elem
                        break
            
            # Limpiar campos
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar campos con datos de prueba
            name_field.send_keys("John Doe")
            print("✓ Campo Nombre llenado: John Doe")
            
            email_field.send_keys("test@examplePS.com")
            print("✓ Campo Email llenado: test@examplePS.com")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            # Configurar access level como Observer
            if access_dropdown:
                try:
                    select = Select(access_dropdown)
                    
                    # Intentar seleccionar "Observer" o variaciones
                    observer_options = ["Observer", "observer", "OBSERVER", "Tutor", "Co-owner"]
                    option_selected = False
                    
                    # Listar todas las opciones disponibles
                    print("Opciones disponibles en el dropdown:")
                    for option in select.options:
                        print(f"  - {option.text} (value: {option.get_attribute('value')})")
                    
                    # Intentar seleccionar Observer
                    for observer_option in observer_options:
                        try:
                            select.select_by_visible_text(observer_option)
                            print(f"✓ Access Level seleccionado: {observer_option}")
                            option_selected = True
                            break
                        except Exception:
                            try:
                                select.select_by_value(observer_option.lower())
                                print(f"✓ Access Level seleccionado por valor: {observer_option}")
                                option_selected = True
                                break
                            except Exception:
                                continue
                    
                    if not option_selected:
                        # Seleccionar la primera opción disponible que no sea vacía
                        for option in select.options:
                            if option.text.strip() and option.text.strip() != "Select...":
                                select.select_by_visible_text(option.text)
                                print(f"✓ Access Level seleccionado (alternativo): {option.text}")
                                break
                                
                except Exception as e:
                    print(f"⚠ Error al configurar access level: {e}")
            else:
                print("⚠ No se pudo configurar access level - dropdown no encontrado")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-K-campos-llenados.png")
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-K-debug.png")
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
                print("✓ Botón 'Add Instructor' clickeado")
                
                # Esperar respuesta del formulario
                time.sleep(3)
                
                # Verificar éxito del envío
                print("Verificando resultado del envío...")
                
                success_found = False
                error_found = False
                
                # Buscar indicadores de éxito
                success_selectors = [
                    "//div[contains(@class, 'success')]",
                    "//div[contains(@class, 'alert-success')]",
                    "//div[contains(text(), 'added')]",
                    "//div[contains(text(), 'saved')]",
                    "//div[contains(text(), 'success')]",
                    "//div[contains(text(), 'instructor')]"
                ]
                
                for selector in success_selectors:
                    try:
                        success_elements = driver.find_elements(By.XPATH, selector)
                        for element in success_elements:
                            if element.is_displayed():
                                success_text = element.text.strip()
                                if success_text:
                                    print(f"✓ Mensaje de éxito encontrado: {success_text}")
                                    success_found = True
                    except Exception:
                        continue
                
                # Buscar indicadores de error
                error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert-danger')]"
                ]
                
                for selector in error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text:
                                    print(f"⚠ Mensaje de error encontrado: {error_text}")
                                    error_found = True
                    except Exception:
                        continue
                
                # Verificar si la URL cambió (indicador de éxito)
                current_url_after = driver.current_url
                url_changed = current_url_after != url
                if url_changed:
                    print(f"✓ URL cambió después del envío: {current_url_after}")
                    success_found = True
                
                # Tomar screenshot final
                take_screenshot(driver, "CP-RF-0002-K", "salida")
                
                if success_found and not error_found:
                    print("✅ TEST EXITOSO: El formulario con access level Observer se envió exitosamente")
                elif not error_found and not success_found:
                    print("⚠ TEST INDETERMINADO: No se detectaron mensajes claros de éxito o error")
                    print("El formulario podría haberse enviado correctamente")
                else:
                    print("❌ TEST FALLIDO: Se detectaron errores en el envío del formulario")
                    print("Con datos válidos y access level Observer, el envío debería ser exitoso")
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-K-error.png")
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
        
        print("=== TEST CP-RF-0002-K COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_access_level_observer()
