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

def test_nombre_con_numeros():
    """
    CP-RF-0002-G: Nombre con números
    RF-0002: Partición de equivalencia
    Verificar validación de campo Nombre con números
    """
    print("=== INICIANDO TEST CP-RF-0002-G ===")
    print("Objetivo: Verificar validación de campo Nombre con números")
    print("Datos de prueba:")
    print("  Nombre: \"John123\"")
    print("  Email: \"test@example.com\"")
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
        screenshot_path = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-G-entrada.png")
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
            
            # Limpiar campos
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar campos con datos de prueba
            # Nombre con números (inválido)
            name_field.send_keys("John123")
            print("✓ Campo Nombre llenado: John123 (contiene números)")
            
            email_field.send_keys("test@example.com")
            print("✓ Campo Email llenado: test@example.com")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-G-campos-llenados.png")
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-G-debug.png")
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
                
                # Verificar mensajes de error para nombre con números
                print("Verificando mensajes de validación...")
                
                error_found = False
                error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//span[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert')]",
                    "//div[contains(text(), 'invalid')]",
                    "//div[contains(text(), 'name')]",
                    "//div[contains(text(), 'number')]"
                ]
                
                for selector in error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text:
                                    print(f"✓ Mensaje de error encontrado: {error_text}")
                                    error_found = True
                    except Exception:
                        continue
                
                # Verificar si el campo nombre tiene indicadores de error
                try:
                    name_field_class = name_field.get_attribute("class")
                    if "error" in name_field_class or "invalid" in name_field_class:
                        print("✓ Campo nombre marcado con clase de error")
                        error_found = True
                except Exception:
                    pass
                
                # Tomar screenshot final
                screenshot_path_final = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-G-salida.png")
                driver.save_screenshot(screenshot_path_final)
                print(f"Screenshot final: {screenshot_path_final}")
                
                if error_found:
                    print("✅ TEST EXITOSO: Se detectó validación de nombre con números")
                else:
                    print("❌ TEST FALLIDO: No se detectó validación de nombre con números")
                    print("El sistema debería rechazar nombres que contengan números")
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-G-error.png")
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
        
        print("=== TEST CP-RF-0002-G COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_nombre_con_numeros()
