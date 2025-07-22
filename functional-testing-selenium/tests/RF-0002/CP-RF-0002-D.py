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

def test_display_desactivado():
    """
    CP-RF-0002-D: Display desactivado, texto en input
    RF-0002: Tabla de Decisiones
    Verificar comportamiento del input con Display desactivado
    """
    print("=== INICIANDO TEST CP-RF-0002-D ===")
    print("Objetivo: Verificar comportamiento del input con Display desactivado")
    print("Datos de prueba:")
    print("  Nombre: \"John Doe\"")
    print("  Email: \"test@example.com\"")
    print("  Display: Desactivado")
    print("  Access: \"Co-owner\"")
    print("")
    
    # Cerrar Chrome antes de empezar
    close_chrome_processes()
    
    try:
        # Crear WebDriver usando driver_setup        driver = get_driver()
        wait = WebDriverWait(driver, 10)
        
        # Agregar script para evitar detección de automatización
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navegar directamente al curso (las cookies se cargan automáticamente)
        url = "https://modern-vortex-463217-h9.appspot.com/web/instructor/courses/edit?courseid=PS"        driver.get(url)
        
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
                time.sleep(2)        else:        # Tomar screenshot inicial
        screenshot_path = os.path.join(os.path.dirname(__file__), "img", "IMG-1-CP-RF-0002-D.png")
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
            display_checkbox = driver.find_element(By.ID, "checkbox-display-instructor-1")
            
            print("✓ Todos los campos encontrados")
            
            # Limpiar campos
            name_field.clear()
            email_field.clear()
            display_field.clear()
            
            # Llenar campos básicos
            name_field.send_keys("John Doe")
            print("✓ Campo Nombre llenado: John Doe")
            
            email_field.send_keys("test@example.com")
            print("✓ Campo Email llenado: test@example.com")
            
            # Verificar estado del checkbox y desactivarlo si está activado
            is_checked = display_checkbox.is_selected()
            print(f"Estado inicial del checkbox Display: {'Activado' if is_checked else 'Desactivado'}")
            
            if is_checked:
                display_checkbox.click()
                print("✓ Checkbox Display desactivado")
                time.sleep(1)  # Esperar a que el cambio tome efecto
            else:
                print("✓ Checkbox Display ya estaba desactivado")
            
            # Verificar que el campo Display Name esté deshabilitado
            is_display_enabled = display_field.is_enabled()
            print(f"Campo Display Name habilitado: {is_display_enabled}")
            
            # Intentar escribir en el campo Display Name (debería estar deshabilitado)
            text_to_write = "Texto de prueba"
            written_text = ""
            
            try:
                # Guardar el valor inicial
                initial_value = display_field.get_attribute("value") or ""
                
                # Intentar escribir
                display_field.click()
                display_field.send_keys(text_to_write)
                
                # Verificar qué se escribió realmente
                final_value = display_field.get_attribute("value") or ""
                written_text = final_value.replace(initial_value, "").strip()
                
                print(f"Texto inicial: '{initial_value}'")
                print(f"Texto después de escribir: '{final_value}'")
                print(f"Texto añadido: '{written_text}'")
                
            except Exception as e:
                print(f"Error al escribir en campo deshabilitado: {e}")
            
            # Hacer clic en "Add Instructor"
            add_instructor_button = driver.find_element(By.ID, "btn-save-instructor-1")
            add_instructor_button.click()
            print("✓ Clic en 'Add Instructor'")
            
            # Esperar respuesta del formulario
            time.sleep(3)
            
            # Verificar si el formulario se envió o no
            current_url_after = driver.current_url
            
            # Buscar indicadores de éxito o error
            success_indicators = driver.find_elements(By.XPATH, "//*[contains(@class, 'success') or contains(@class, 'alert-success')]")
            error_indicators = driver.find_elements(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'alert-danger')]")
            
            # Evaluar resultado basado en múltiples factores
            if not is_display_enabled and (not written_text or written_text == ""):
                if not success_indicators:
                    resultado = "TEST EXITOSO: Campo Display deshabilitado correctamente, no permite texto, formulario no se envió"
                else:
                    resultado = "TEST PARCIAL: Campo deshabilitado pero formulario se envió inesperadamente"
            elif not is_display_enabled and written_text:
                resultado = "TEST PARCIAL: Campo deshabilitado pero permitió escribir texto"
            elif is_display_enabled:
                resultado = "TEST FALLIDO: Campo Display no se deshabilitó al desactivar checkbox"
            else:
                resultado = "TEST INCONCLUSO: No se pudo determinar el comportamiento esperado"
            
            print(f"Evaluación:")
            print(f"  - Campo deshabilitado: {not is_display_enabled}")
            print(f"  - Texto escrito: '{written_text}'")
            print(f"  - Indicadores de éxito: {len(success_indicators)}")
            print(f"  - Indicadores de error: {len(error_indicators)}")
            
        except Exception as e:
            print(f"✗ Error al interactuar con el formulario: {e}")
            resultado = "TEST FALLIDO: Error al interactuar con el formulario"
        
        # Tomar screenshot final
        final_screenshot_path = os.path.join(os.path.dirname(__file__), "img", "IMG-2-CP-RF-0002-D.png")
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
            driver.quit()if __name__ == "__main__":
    resultado = test_display_desactivado()
    print(f"\nResultado final: {resultado}")
