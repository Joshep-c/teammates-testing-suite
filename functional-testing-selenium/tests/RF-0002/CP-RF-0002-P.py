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

def test_boundary_analysis_100_chars():
    """
    CP-RF-0002-P: Análisis de límites - 100 caracteres en nombre
    RF-0002: Tabla de decisiones
    Verificar comportamiento con nombre de 100 caracteres (límite exacto)
    """
    print("=== INICIANDO TEST CP-RF-0002-P ===")
    print("Objetivo: Verificar comportamiento con nombre de 100 caracteres (límite exacto)")
    print("Datos de prueba:")
    
    # Crear nombre de exactamente 100 caracteres
    name_100_chars = "B" * 100
    print(f"  Nombre: \"{name_100_chars}\" (100 caracteres)")
    print(f"  Longitud del nombre: {len(name_100_chars)} caracteres")
    print("  Email: \"limit.test@example.com\"")
    print("  Display: \"Limit Test\"")
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
        take_screenshot(driver, "CP-RF-0002-P", "entrada")
        
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
            name_field.send_keys(name_100_chars)
            print(f"✓ Campo Nombre llenado con {len(name_100_chars)} caracteres")
            
            # Verificar que se aceptó todo el texto
            actual_name_value = name_field.get_attribute("value")
            actual_length = len(actual_name_value)
            print(f"   Longitud real en el campo: {actual_length} caracteres")
            
            if actual_length == 100:
                print("✓ PERFECTO: Se aceptaron todos los 100 caracteres")
            elif actual_length < 100:
                print(f"⚠ TRUNCADO: Solo se aceptaron {actual_length} de 100 caracteres")
                print(f"   Límite real del campo: {actual_length} caracteres")
            else:
                print(f"⚠ INESPERADO: Se aceptaron {actual_length} caracteres (más de 100)")
            
            email_field.send_keys("limit.test@example.com")
            print("✓ Campo Email llenado: limit.test@example.com")
            
            display_field.send_keys("Limit Test")
            print("✓ Campo Display llenado: Limit Test")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-P-campos-llenados.png")
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-P-debug.png")
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
                
                # Verificar mensajes de error específicos de límite
                errors_found = []
                error_selectors = [
                    "//div[contains(@class, 'error')]",
                    "//span[contains(@class, 'error')]",
                    "//div[contains(@class, 'invalid')]",
                    "//span[contains(@class, 'invalid')]",
                    "//div[contains(@class, 'alert-danger')]",
                    "//div[contains(text(), 'length')]",
                    "//div[contains(text(), 'limit')]",
                    "//div[contains(text(), 'character')]",
                    "//div[contains(text(), 'maximum')]",
                    "//div[contains(text(), 'too long')]"
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
                take_screenshot(driver, "CP-RF-0002-P", "salida")
                
                # Evaluar resultados con análisis detallado
                print("\n📊 ANÁLISIS DETALLADO DEL LÍMITE:")
                print(f"   • Caracteres enviados: {len(name_100_chars)}")
                print(f"   • Caracteres aceptados: {actual_length}")
                
                if actual_length < 100:
                    print(f"   • LÍMITE IDENTIFICADO: {actual_length} caracteres máximo")
                    print(f"   • Truncamiento automático aplicado")
                elif actual_length == 100:
                    print("   • Campo acepta exactamente 100 caracteres")
                
                if len(success_indicators) > 0:
                    if actual_length == 100:
                        print("\n✅ TEST EXITOSO: Límite exacto de 100 caracteres confirmado")
                        print("El sistema acepta exactamente 100 caracteres")
                    else:
                        print(f"\n✅ TEST EXITOSO: Límite de {actual_length} caracteres confirmado")
                        print(f"El texto fue truncado a {actual_length} caracteres y aceptado")
                    
                    for msg in success_indicators:
                        print(f"   • {msg}")
                        
                elif url_changed:
                    print("\n✅ TEST EXITOSO: URL cambió, indicando envío exitoso")
                    if actual_length == 100:
                        print("100 caracteres está dentro del límite permitido")
                    else:
                        print(f"Campo truncó a {actual_length} caracteres automáticamente")
                        
                elif len(errors_found) == 0:
                    print("\n✅ TEST EXITOSO: No se detectaron errores de longitud")
                    if actual_length == 100:
                        print("100 caracteres es el límite exacto aceptable")
                    else:
                        print(f"Campo maneja límite automáticamente ({actual_length} caracteres)")
                        
                elif len(errors_found) > 0:
                    if actual_length == 100:
                        print("\n❌ TEST LÍMITE ALCANZADO: 100 caracteres genera error")
                        print("El límite máximo es menor a 100 caracteres")
                    else:
                        print(f"\n⚠ COMPORTAMIENTO MIXTO: Campo truncó pero mostró errores")
                        
                    for error in errors_found:
                        print(f"   • {error}")
                
                # Conclusión del análisis de límites
                print("\n🎯 CONCLUSIÓN DEL ANÁLISIS:")
                if actual_length == len(name_100_chars) and len(success_indicators) > 0:
                    print("   • Límite máximo: >= 100 caracteres")
                    print("   • Comportamiento: Acepta 100 caracteres completamente")
                elif actual_length < len(name_100_chars):
                    print(f"   • Límite máximo: {actual_length} caracteres")
                    print(f"   • Comportamiento: Truncamiento automático")
                else:
                    print("   • Límite necesita análisis adicional")
                        
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-P-error.png")
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
        
        print("=== TEST CP-RF-0002-P COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_boundary_analysis_100_chars()
