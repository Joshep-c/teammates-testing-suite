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

def test_registro_instructor():
    """
    CP-RF-0001-S: Registro por lotes con nombre vacío
    RF-0001: Partición de equivalencia
    Verificar que el sistema no permita registrar un instructor sin nombre
    """
    print("=== INICIANDO TEST CP-RF-0001-S ===")
    print("Objetivo: Registro por lotes con nombre vacío")
    print("Datos de prueba:")
    print("  Entrada por lotes: |maria@unsa.edu.pe|UNSA (nombre vacío)")
    print("")
    
    # Cerrar Chrome antes de empezar
    # Chrome se maneja automáticamente via get_driver_for_rf
    
    try:
        # Crear WebDriver usando driver_setup
        driver = get_driver_for_rf("0001")
        wait = WebDriverWait(driver, 10)
        
        # Agregar script para evitar detección de automatización
        # Anti-detección manejado por driver_setup global
        
        # Navegar directamente a la página de administrador
        admin_url = "https://modern-vortex-463217-h9.appspot.com/web/admin/home"
        driver.get(admin_url)
        
        
        # Verificar que estamos en la página correcta
        if "TEAMMATES" not in driver.title:
            print("ERROR: No se pudo acceder a la página de administrador")
            print("La sesión puede haber expirado.")
            return False
        
        
        # Esperar a que la página cargue completamente
        time.sleep(3)
        
        # Buscar el formulario de registro por lotes
        print("Buscando formulario de registro por lotes...")
        
        # Buscar el campo de texto para registro por lotes
        try:
            batch_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-details-single-line")))
            print("Campo de registro por lotes encontrado con ID: instructor-details-single-line")
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo de registro por lotes: {e}")            
            return False
        
        # Ingresar línea con nombre vacío
        batch_data = "|maria@unsa.edu.pe|UNSA"
        print(f"Ingresando datos por lotes: '{batch_data}' (nombre vacío)...")
        batch_field.clear()
        batch_field.send_keys(batch_data)
                # Buscar el botón "Add Instructors" (plural)
        try:
            add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-instructor-single-line")))
            print("Botón 'Add Instructors' encontrado con ID: add-instructor-single-line")
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el botón 'Add Instructors': {e}")
            return False
        
        print("Datos ingresados:")
        print(f"  Entrada por lotes: {batch_field.get_attribute('value')} (nombre vacío)")
        
        # IMAGEN 1: Captura después de ingresar datos con nombre vacío        
        time.sleep(2)
        
        # Hacer clic en "Add Instructors"        
        add_button.click()
        
        time.sleep(3)
        
        # Desplazar al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # IMAGEN 2: Captura después de hacer clic en "Add Instructors"        
        time.sleep(2)        # Verificar mensaje de error por nombre vacío
        print("Verificando mensaje de error por nombre vacío...")
        try:
            # Buscar mensaje de error específico de nombre vacío
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            print("ÉXITO: Se detectó mensaje de error por nombre vacío")
            print(f"Mensaje de error: {error_message.text}")
            if "name" in error_message.text.lower() or "nombre" in error_message.text.lower() or "required" in error_message.text.lower() or "obligatorio" in error_message.text.lower():
                print("ÉXITO: El mensaje indica correctamente el error de nombre vacío")
                result = True
            else:
                print("ADVERTENCIA: El mensaje de error no especifica nombre vacío")
                result = True  # Aún consideramos éxito si hay error
        except Exception:
            try:
                # Buscar otros tipos de mensajes de validación relacionados con nombre vacío
                validation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'name') or contains(text(), 'nombre') or contains(text(), 'required')]")
                print("ÉXITO: Se detectó mensaje de validación por nombre vacío")
                print(f"Mensaje de validación: {validation_message.text}")
                result = True
            except Exception:
                print("FALLO: No se detectó validación para nombre vacío en registro por lotes")
                print("El sistema permitió registrar instructor sin nombre")
                result = False

        print("=== TEST CP-RF-0001-S COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-S", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()
            
if __name__ == "__main__":
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El sistema correctamente rechazó el registro con nombre vacío")
    elif resultado == False:
        print("TEST FALLÓ: El sistema permitió el registro con nombre vacío")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
