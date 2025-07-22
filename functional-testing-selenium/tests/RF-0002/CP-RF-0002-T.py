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

def test_email_boundary_255_chars():
    """
    CP-RF-0002-T: Análisis de límites - Email con 255 caracteres
    RF-0002: Tabla de decisiones
    Verificar validación con email de 255 caracteres (inmediatamente superior a 254)
    """
    print("=== INICIANDO TEST CP-RF-0002-T ===")
    print("Objetivo: Verificar validación con email de 255 caracteres (inmediatamente superior)")
    print("Datos de prueba:")
    
    # Crear email de exactamente 255 caracteres
    # "a" x 243 + "@example.com" = 243 + 12 = 255 caracteres
    email_prefix = "a" * 243
    email_255_chars = email_prefix + "@example.com"
    
    print("  Nombre: \"John Doe\"")
    print(f"  Email: \"{email_prefix[:20]}...@example.com\" (255 caracteres)")
    print(f"  Longitud del email: {len(email_255_chars)} caracteres")
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
        take_screenshot(driver, "CP-RF-0002-T", "entrada")
        
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
            name_field.send_keys("John Doe")
            print("✓ Campo Nombre llenado: John Doe")
            
            # Llenar email con 255 caracteres
            email_field.send_keys(email_255_chars)
            print(f"✓ Campo Email llenado con {len(email_255_chars)} caracteres")
            
            # Verificar que se aceptó todo el texto del email o se truncó
            actual_email_value = email_field.get_attribute("value")
            actual_email_length = len(actual_email_value)
            print(f"   Longitud real del email en el campo: {actual_email_length} caracteres")
            
            if actual_email_length == 255:
                print("⚠ CAMPO ACEPTA 255 CARACTERES: El límite podría ser mayor a 254")
            elif actual_email_length == 254:
                print("✓ TRUNCAMIENTO A 254: Límite máximo confirmado en 254 caracteres")
            elif actual_email_length < 254:
                print(f"✓ TRUNCAMIENTO A {actual_email_length}: Límite máximo identificado")
            else:
                print(f"⚠ COMPORTAMIENTO INESPERADO: {actual_email_length} caracteres aceptados")
            
            display_field.send_keys("Instructor")
            print("✓ Campo Display llenado: Instructor")
            
            # Tomar screenshot después de llenar campos
            screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-T-campos-llenados.png")
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
                screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-T-debug.png")
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
                
                # Verificar mensajes de error específicos de email con límite de 255
                email_errors_found = []
                email_error_selectors = [
                    "//div[contains(@class, 'error') and contains(text(), 'email')]",
                    "//span[contains(@class, 'error') and contains(text(), 'email')]",
                    "//div[contains(@class, 'invalid') and contains(text(), 'email')]",
                    "//div[contains(text(), 'email') and (contains(text(), 'length') or contains(text(), 'limit') or contains(text(), 'character'))]",
                    "//div[contains(text(), 'length') and contains(text(), 'email')]",
                    "//div[contains(text(), '254') and contains(text(), 'email')]",
                    "//div[contains(text(), '255') and contains(text(), 'email')]",
                    "//div[contains(text(), 'email') and contains(text(), 'too long')]",
                    "//div[contains(text(), 'email') and contains(text(), 'exceed')]",
                    "//div[contains(text(), 'email') and contains(text(), 'maximum')]",
                    "//div[contains(text(), 'email') and contains(text(), 'cannot')]"
                ]
                
                for selector in email_error_selectors:
                    try:
                        error_elements = driver.find_elements(By.XPATH, selector)
                        for element in error_elements:
                            if element.is_displayed():
                                error_text = element.text.strip()
                                if error_text and error_text not in email_errors_found:
                                    print(f"✓ Error de límite de email encontrado: {error_text}")
                                    email_errors_found.append(error_text)
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
                                if error_text and error_text not in general_errors_found and error_text not in email_errors_found:
                                    print(f"⚠ Error general encontrado: {error_text}")
                                    general_errors_found.append(error_text)
                    except Exception:
                        continue
                
                # Verificar si el campo email tiene clase de error
                email_field_has_error = False
                try:
                    email_field_class = email_field.get_attribute("class")
                    if "error" in email_field_class or "invalid" in email_field_class:
                        print("✓ Campo email marcado visualmente con error")
                        email_field_has_error = True
                except Exception:
                    pass
                
                # Verificar indicadores de éxito (no esperados para 255 caracteres)
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
                                    print(f"⚠ Mensaje de éxito encontrado (inesperado): {success_text}")
                                    success_indicators.append(success_text)
                    except Exception:
                        continue
                
                # Verificar si la URL cambió (indicador de éxito no esperado)
                new_url = driver.current_url
                url_changed = new_url != url
                
                # Tomar screenshot final
                take_screenshot(driver, "CP-RF-0002-T", "salida")
                
                # Evaluar resultados con análisis detallado para 255 caracteres
                print("\n📊 ANÁLISIS DETALLADO DEL EMAIL (255 CARACTERES - SUPERIOR AL LÍMITE):")
                print(f"   • Caracteres enviados: {len(email_255_chars)}")
                print(f"   • Caracteres aceptados en campo: {actual_email_length}")
                print(f"   • Errores específicos de email: {len(email_errors_found)}")
                print(f"   • Campo marcado como error: {email_field_has_error}")
                print(f"   • Indicadores de éxito: {len(success_indicators)}")
                print(f"   • URL cambió: {url_changed}")
                
                # Lógica de evaluación específica para 255 caracteres (debería ser rechazado)
                if len(email_errors_found) > 0 or email_field_has_error:
                    print("\n✅ TEST EXITOSO: Email de 255 caracteres rechazado correctamente")
                    print("El sistema detecta y rechaza emails superiores a 254 caracteres")
                    for error in email_errors_found:
                        print(f"   • {error}")
                    
                elif actual_email_length < 255 and len(success_indicators) > 0:
                    print(f"\n✅ TEST EXITOSO: Email truncado a {actual_email_length} caracteres y aceptado")
                    print("El sistema maneja el límite mediante truncamiento automático")
                    
                elif actual_email_length < 255 and len(general_errors_found) == 0:
                    print(f"\n✅ TEST PARCIALMENTE EXITOSO: Email truncado a {actual_email_length} caracteres")
                    print("El límite se maneja por truncamiento silencioso")
                    
                elif len(success_indicators) > 0 and actual_email_length == 255:
                    print("\n❌ TEST FALLIDO: El sistema acepta 255 caracteres")
                    print("PROBLEMA: El límite de 254 caracteres no se está aplicando")
                    
                elif url_changed and actual_email_length == 255:
                    print("\n❌ TEST FALLIDO: Formulario enviado con 255 caracteres")
                    print("PROBLEMA: El límite de 254 caracteres no se está validando")
                    
                elif len(general_errors_found) == 0 and len(email_errors_found) == 0:
                    print("\n❌ TEST FALLIDO: No se detectaron errores con 255 caracteres")
                    print("El sistema debería rechazar emails de 255 caracteres")
                    
                else:
                    print("\n⚠ TEST INDETERMINADO: Comportamiento del límite no claro")
                    print("Se requiere análisis manual adicional")
                
                # Conclusión específica para el límite superior (255 caracteres)
                print("\n🎯 CONCLUSIÓN DEL ANÁLISIS DE LÍMITE SUPERIOR (255):")
                if len(email_errors_found) > 0:
                    print("   • 255 caracteres: RECHAZADO ✓ (límite funcionando correctamente)")
                    print("   • Límite máximo confirmado: 254 caracteres")
                    print("   • Comportamiento: Validación con mensajes de error")
                elif actual_email_length < 255:
                    print(f"   • Límite máximo identificado: {actual_email_length} caracteres")
                    print("   • Comportamiento: Truncamiento automático")
                elif len(success_indicators) > 0:
                    print("   • 255 caracteres: ACEPTADO ❌ (problema de validación)")
                    print("   • Límite máximo: > 254 caracteres (inesperado)")
                else:
                    print("   • Límite de validación requiere verificación adicional")
                
                # Resumen comparativo final
                print("\n📈 RESUMEN COMPARATIVO DEL ANÁLISIS DE LÍMITES DE EMAIL:")
                print("   • CP-RF-0002-R (253 chars): Debería ser ACEPTADO")
                print("   • CP-RF-0002-S (254 chars): Debería ser ACEPTADO (límite exacto)")
                print("   • CP-RF-0002-T (255 chars): Debería ser RECHAZADO ← TEST ACTUAL")
                
                if len(email_errors_found) > 0:
                    print("   ✅ VALIDACIÓN FUNCIONANDO: El límite de 254 caracteres se está aplicando")
                elif actual_email_length <= 254:
                    print("   ⚠ TRUNCAMIENTO SILENCIOSO: El límite se aplica automáticamente")
                else:
                    print("   ❌ PROBLEMA DE VALIDACIÓN: El límite de 254 caracteres no se aplica")
                        
            else:
                print("❌ No se pudo encontrar botón para enviar el formulario")
                
        except Exception as e:
            print(f"❌ Error al interactuar con el formulario: {e}")
            screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "CP-RF-0002-T-error.png")
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
        
        print("=== TEST CP-RF-0002-T COMPLETADO ===")
        print("")

if __name__ == "__main__":
    test_email_boundary_255_chars()
