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

def test_boundary_analysis_101_chars():
    """
    CP-RF-0002-Q: Análisis de límites - 101 caracteres en nombre
    RF-0002: Tabla de decisiones
    Verificar validación con longitud mayor a 100 caracteres
    """
    print("=== INICIANDO TEST CP-RF-0002-Q ===")
    print("Objetivo: Verificar validación con nombre de 101 caracteres (inmediatamente superior)")
    print("Datos de prueba:")
    
    # Crear nombre de exactamente 101 caracteres
    name_101_chars = "a" * 101
    print(f"  Nombre: \"{name_101_chars[:20]}...\" (101 caracteres)")
    print(f"  Longitud del nombre: {len(name_101_chars)} caracteres")
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
        take_screenshot(driver, "CP-RF-0002-Q", "entrada")
        
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
            name_field.send_keys(name_101_chars)
            print(f"✓ Campo Nombre llenado con {len(name_101_chars)} caracteres")
            
            # Verificar que se aceptó todo el texto o se truncó
            actual_name_value = name_field.get_attribute("value")
            actual_length = len(actual_name_value)
            print(f"   Longitud real en el campo: {actual_length} caracteres")
            
            if actual_length == 101:
                print("⚠ CAMPO ACEPTA 101 CARACTERES: El límite podría ser mayor")
            elif actual_length == 100:
                print("✓ TRUNCAMIENTO A 100: Límite máximo confirmado en 100 caracteres")
            elif actual_length < 100:
                print(f"✓ TRUNCAMIENTO A {actual_length}: Límite máximo identificado")
            else:
                print(f"⚠ COMPORTAMIENTO INESPERADO: {actual_length} caracteres aceptados")
            
            email_field.send_keys("test@example.com")
            print("✓ Campo Email llenado: test@example.com")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-Q-campos-llenados.png")
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-Q-debug.png")
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
                
                # Verificar mensajes de error específicos de límite en nombre
                name_errors_found = []
                name_error_selectors = [
                    "//div[contains(@class, 'error') and contains(text(), 'name')]",
                    "//span[contains(@class, 'error') and contains(text(), 'name')]",
                    "//div[contains(@class, 'invalid') and contains(text(), 'name')]",
                    "//div[contains(text(), 'name') and (contains(text(), 'length') or contains(text(), 'limit') or contains(text(), 'character'))]",
                    "//div[contains(text(), 'length') and contains(text(), 'name')]",
                    "//div[contains(text(), 'character') and contains(text(), 'name')]",
                    "//div[contains(text(), '100') and contains(text(), 'name')]",
                    "//div[contains(text(), 'too long')]",
                    "//div[contains(text(), 'exceed')]"
                ]
                
                for selector in name_error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text and error_text not in name_errors_found:
                                    print(f"✓ Error de límite de nombre encontrado: {error_text}")
                                    name_errors_found.append(error_text)
                    except Exception:
                        continue
                
                # Verificar errores generales
                general_errors_found = []
                general_error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert-danger')]"
                ]
                
                for selector in general_error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text and error_text not in general_errors_found and error_text not in name_errors_found:
                                    print(f"⚠ Error general encontrado: {error_text}")
                                    general_errors_found.append(error_text)
                    except Exception:
                        continue
                
                # Verificar si el campo nombre tiene clase de error
                name_field_has_error = False
                try:
                    name_field_class = name_field.get_attribute("class")
                    if "error" in name_field_class or "invalid" in name_field_class:
                        print("✓ Campo nombre marcado visualmente con error")
                        name_field_has_error = True
                except Exception:
                    pass
                
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
                                    print(f"⚠ Mensaje de éxito encontrado: {success_text}")
                                    success_indicators.append(success_text)
                    except Exception:
                        continue
                
                # Verificar si la URL cambió (indicador de éxito)
                new_url = driver.current_url
                url_changed = new_url != url
                
                # Tomar screenshot final
                take_screenshot(driver, "CP-RF-0002-Q", "salida")
                
                # Evaluar resultados con análisis detallado
                print("\n📊 ANÁLISIS DETALLADO DEL LÍMITE (101 CARACTERES):")
                print(f"   • Caracteres enviados: {len(name_101_chars)}")
                print(f"   • Caracteres aceptados en campo: {actual_length}")
                print(f"   • Errores específicos de nombre: {len(name_errors_found)}")
                print(f"   • Campo marcado como error: {name_field_has_error}")
                print(f"   • Indicadores de éxito: {len(success_indicators)}")
                
                # Lógica de evaluación
                if len(name_errors_found) > 0 or name_field_has_error:
                    print("\n✅ TEST EXITOSO: Validación de límite funciona correctamente")
                    print("El sistema detecta y rechaza nombres de 101 caracteres")
                    for error in name_errors_found:
                        print(f"   • {error}")
                    
                elif actual_length < 101 and len(success_indicators) > 0:
                    print(f"\n✅ TEST EXITOSO: Truncamiento automático a {actual_length} caracteres")
                    print("El sistema maneja el límite mediante truncamiento silencioso")
                    
                elif actual_length < 101 and len(general_errors_found) == 0:
                    print(f"\n✅ TEST PARCIALMENTE EXITOSO: Truncamiento a {actual_length} caracteres")
                    print("El límite se maneja por truncamiento, pero sin validación visible")
                    
                elif len(success_indicators) > 0 and actual_length == 101:
                    print("\n❌ TEST FALLIDO: El sistema acepta 101 caracteres")
                    print("PROBLEMA: El límite de 100 caracteres no se está aplicando")
                    
                elif url_changed and actual_length == 101:
                    print("\n❌ TEST FALLIDO: Formulario enviado con 101 caracteres")
                    print("PROBLEMA: El límite de 100 caracteres no se está validando")
                    
                else:
                    print("\n⚠ TEST INDETERMINADO: Comportamiento del límite no claro")
                    print("Se requiere análisis manual adicional")
                
                # Conclusión específica del límite
                print("\n🎯 CONCLUSIÓN DEL ANÁLISIS DE LÍMITE:")
                if actual_length == 100:
                    print("   • Límite máximo confirmado: 100 caracteres")
                    print("   • Comportamiento: Truncamiento automático")
                elif actual_length < 100:
                    print(f"   • Límite máximo identificado: {actual_length} caracteres")
                    print("   • Comportamiento: Truncamiento automático")
                elif len(name_errors_found) > 0:
                    print("   • Límite máximo: 100 caracteres")
                    print("   • Comportamiento: Validación con mensajes de error")
                else:
                    print("   • Límite requiere validación adicional")
                        
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-Q-error.png")
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
        
        print("=== TEST CP-RF-0002-Q COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_boundary_analysis_101_chars()
