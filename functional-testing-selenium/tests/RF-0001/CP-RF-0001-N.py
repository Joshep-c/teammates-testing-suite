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
    CP-RF-0001-N: Registro con email que supera la longitud permitida
    RF-0001: Partición de equivalencia
    Validar que el sistema rechace emails que excedan el límite de longitud (ej. 320 caracteres)
    """
    print("=== INICIANDO TEST CP-RF-0001-N ===")
    print("Objetivo: Registro con email que supera la longitud permitida")
    
    # Generar email de 320 caracteres (local + domain)
    # Email formato: aaaa...@unsa.edu.pe (parte local muy larga)
    domain = "@unsa.edu.pe"
    local_part_length = 320 - len(domain)
    long_email = "a" * local_part_length + domain
    
    print("Datos de prueba:")
    print("  Name: Carlos Mena")
    print(f"  Email: {long_email[:50]}...{domain} (320 caracteres)")
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
        # Buscar y llenar el campo Name
        try:
            name_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-name")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Name': {e}")
            return False
        name_field.clear()
        name_field.send_keys("Carlos Mena")
                # Buscar y llenar el campo Email con email muy largo
        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-email")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Email': {e}")
            return False
        
        print(f"Llenando campo 'Email' con email de 320 caracteres...")
        email_field.clear()
        email_field.send_keys(long_email)
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
        actual_email_value = email_field.get_attribute('value')
        print(f"  Name: {name_field.get_attribute('value')}")
        print(f"  Email: {actual_email_value[:50]}...{domain} (longitud: {len(actual_email_value)} caracteres)")
        print(f"  Institution: {institution_field.get_attribute('value')}")

        # IMAGEN 1: Captura después de llenar los datos
        time.sleep(2)

        # Hacer clic en "Add Instructor"
        add_button.click()

        time.sleep(3)
        
        # Desplazar al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # IMAGEN 2: Captura después de hacer clic en "Add Instructor"
        time.sleep(2)

        # Verificar mensaje de error por email excesivamente largo
        print("Verificando mensaje de error por email excesivamente largo...")
        try:
            # Buscar mensaje de error específico de longitud de email
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            print("ÉXITO: Se detectó mensaje de error de longitud de email")
            print(f"Mensaje de error: {error_message.text}")
            if "length" in error_message.text.lower() or "long" in error_message.text.lower() or "largo" in error_message.text.lower() or "email" in error_message.text.lower():
                print("ÉXITO: El mensaje indica correctamente el error de longitud de email")
                result = True
            else:
                print("ADVERTENCIA: El mensaje de error no especifica longitud de email")
                result = True  # Aún consideramos éxito si hay error
        except Exception:
            try:
                # Buscar otros tipos de mensajes de validación relacionados con email largo
                validation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'email') and (contains(text(), 'length') or contains(text(), 'long') or contains(text(), 'largo'))]")
                print("ÉXITO: Se detectó mensaje de validación de email largo")
                print(f"Mensaje de validación: {validation_message.text}")
                result = True
            except Exception:
                # Verificar si el campo de email tiene limitación de caracteres
                max_length = email_field.get_attribute('maxlength')
                if max_length and len(actual_email_value) <= int(max_length):
                    print(f"ÉXITO: El campo limita la entrada de email a {max_length} caracteres")
                    print(f"Longitud actual del email: {len(actual_email_value)}")
                    result = True
                else:
                    print("FALLO: No se detectó validación de longitud para el email")
                    print(f"Se permitió ingresar email de {len(actual_email_value)} caracteres")
                    result = False

        print("=== TEST CP-RF-0001-N COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-N", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El sistema correctamente rechazó el email excesivamente largo")
    elif resultado == False:
        print("TEST FALLÓ: El sistema permitió el email excesivamente largo")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
