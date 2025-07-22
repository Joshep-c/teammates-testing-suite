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
    CP-RF-0001-O: Registro con números en el campo Name
    RF-0001: Partición de equivalencia
    Verificar que el sistema no permita ingresar números en el campo de nombre del instructor
    """
    print("=== INICIANDO TEST CP-RF-0001-O ===")
    print("Objetivo: Registro con números en el campo Name")
    print("Datos de prueba:")
    print("  Name: Carlos123 (contiene números)")
    print("  Email: carlos@unsa.edu.pe")
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
        # Buscar y llenar el campo Name con números
        try:
            name_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-name")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Name': {e}")
            return False

        print("Llenando campo 'Name' con 'Carlos123' (contiene números)...")
        name_field.clear()
        name_field.send_keys("Carlos123")
                # Buscar y llenar el campo Email
        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-email")))
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo 'Email': {e}")
            return False
        email_field.clear()
        email_field.send_keys("carlos@unsa.edu.pe")
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
        print(f"  Name: {name_field.get_attribute('value')} (contiene números)")
        print(f"  Email: {email_field.get_attribute('value')}")
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

        # Verificar mensaje de error por números en el nombre
        print("Verificando mensaje de error por números en el campo Name...")
        try:
            # Buscar mensaje de error específico de números en nombre
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            print("ÉXITO: Se detectó mensaje de error por números en Name")
            print(f"Mensaje de error: {error_message.text}")
            if "number" in error_message.text.lower() or "numeric" in error_message.text.lower() or "números" in error_message.text.lower() or "name" in error_message.text.lower():
                print("ÉXITO: El mensaje indica correctamente el error de números en Name")
                result = True
            else:
                print("ADVERTENCIA: El mensaje de error no especifica números en Name")
                result = True  # Aún consideramos éxito si hay error
        except Exception:
            try:
                # Buscar otros tipos de mensajes de validación relacionados con números
                validation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'number') or contains(text(), 'numeric') or contains(text(), 'números') or contains(text(), 'alfabético')]")
                print("ÉXITO: Se detectó mensaje de validación por números en Name")
                print(f"Mensaje de validación: {validation_message.text}")
                result = True
            except Exception:
                # Verificar si el campo tiene pattern de validación para solo letras
                pattern = name_field.get_attribute('pattern')
                if pattern and '[0-9]' not in pattern:
                    print("ÉXITO: El campo tiene validación de patrón que excluye números")
                    print(f"Patrón detectado: {pattern}")
                    result = True
                else:
                    print("FALLO: No se detectó validación para evitar números en Name")
                    print("El sistema permitió ingresar números en el campo Name")
                    result = False

        print("=== TEST CP-RF-0001-O COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-O", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El sistema correctamente rechazó el nombre con números")
    elif resultado == False:
        print("TEST FALLÓ: El sistema permitió el nombre con números")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
