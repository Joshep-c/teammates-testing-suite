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
    CP-RF-0001-C: Registro con campo Email vacío
    RF-0001: Partición de equivalencia
    Verificar que el sistema no permita registrar un instructor con el campo "Email" vacío
    """
    print("=== INICIANDO TEST CP-RF-0001-C ===")
    print("Objetivo: Registro con campo Email vacío")
    print("Datos de prueba:")
    print("  Name: Sergio Ticona")
    print("  Email: (vacío)")
    print("  Institution: UNSA")
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
        
        # Buscar el formulario de registro de instructor        
        # Usar los selectores exactos encontrados en la exploración
        try:
            name_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-name")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Name': {e}")
            return False

        # Limpiar y llenar el campo Name
        name_field.clear()
        name_field.send_keys("Sergio Ticona")
                # Buscar y llenar el campo Email
        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-email")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Email': {e}")
            return False
        email_field.clear()
        # NO se envían datos al campo Email
                # Buscar y llenar el campo Institution
        try:
            institution_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-institution")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Institution': {e}")
            return False
        institution_field.clear()
        institution_field.send_keys("UNSA")
                # Buscar el botón "Add Instructor"
        try:
            add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-instructor")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el botón 'Add Instructor': {e}")
            return False
        
        print("Datos ingresados:")
        print(f"  Name: {name_field.get_attribute('value')}")
        print(f"  Email: '{email_field.get_attribute('value')}' (vacío)")
        print(f"  Institution: {institution_field.get_attribute('value')}")
        
        # IMAGEN 1: Captura después de llenar los datos (Email vacío)        
        time.sleep(2)

        # Hacer clic en "Add Instructor"
        add_button.click()

        time.sleep(2)
        
        # Desplazar al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # IMAGEN 2: Captura después de hacer clic en "Add Instructor"
        # time.sleep(2)  # Esperar un poco para que se procese la acción
        # Verificar mensaje de error
        try:
            # Buscar mensaje de error o validación
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            print("ÉXITO: Se detectó mensaje de error como esperado")
            print(f"Mensaje de error: {error_message.text}")
            result = True
        except:
            try:
                # Buscar otros tipos de mensajes de validación
                validation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'required') or contains(text(), 'obligatorio') or contains(text(), 'Email')]")
                print("ÉXITO: Se detectó mensaje de validación")
                print(f"Mensaje de validación: {validation_message.text}")
                result = True
            except:
                # Verificar si el botón sigue habilitado/deshabilitado
                if add_button.is_enabled():
                    print("FALLO: El sistema permitió enviar el formulario con Email vacío")
                    result = False
                else:
                    print("ÉXITO: El botón está deshabilitado con Email vacío")
                    result = True

        print("=== TEST CP-RF-0001-C COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-C", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":  
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El sistema correctamente rechazó el registro con Email vacío")
    elif resultado == False:
        print("TEST FALLÓ: El sistema permitió el registro con Email vacío")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
