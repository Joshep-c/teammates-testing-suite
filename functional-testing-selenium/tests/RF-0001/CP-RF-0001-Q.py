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
    CP-RF-0001-Q: Registro por lotes exitoso con una línea válida
    RF-0001: Partición de equivalencia
    Verificar que se pueda registrar correctamente un instructor por lote
    """
    print("=== INICIANDO TEST CP-RF-0001-Q ===")
    print("Objetivo: Registro por lotes exitoso con una línea válida")
    print("Datos de prueba:")
    print("  Línea: Juan Pérez|juan.perez@unsa.edu.pe|UNSA")
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
        
        # Buscar el campo textarea para registro por lotes
        try:
            batch_field = wait.until(EC.presence_of_element_located((By.ID, "instructor-details-single-line")))
            print("Campo de registro por lotes encontrado con ID: instructor-details-single-line")
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el campo de registro por lotes: {e}")
            return False
        
        # Limpiar y llenar el campo de registro por lotes
        batch_data = "Juan Pérez|juan.perez@unsa.edu.pe|UNSA"
        print(f"Llenando campo de registro por lotes con: '{batch_data}'...")
        batch_field.clear()
        batch_field.send_keys(batch_data)
                # Buscar el botón "Add Instructors" (para registro por lotes)
        try:
            add_batch_button = wait.until(EC.element_to_be_clickable((By.ID, "add-instructor-single-line")))
            print("Botón 'Add Instructors' encontrado con ID: add-instructor-single-line")
        except Exception as e:
            print(f"ERROR: No se pudo encontrar el botón 'Add Instructors': {e}")
            return False
        
        print("Datos ingresados:")
        print(f"  Línea de registro: {batch_field.get_attribute('value')}")
        
        # IMAGEN 1: Captura después de llenar los datos por lotes        
        
        time.sleep(2)

        # Hacer clic en "Add Instructors"
        add_batch_button.click()

        time.sleep(3)
        
        # Desplazar al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # IMAGEN 2: Captura después de hacer clic en "Add Instructors"
        time.sleep(2)

        # Verificar el resultado del registro por lotes
        print("Verificando resultado del registro por lotes...")
        try:
            # Buscar mensaje de éxito
            success_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
            print("ÉXITO: Se detectó mensaje de éxito")
            print(f"Mensaje de éxito: {success_message.text}")
            result = True
        except:
            try:
                # Buscar mensaje de error
                error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
                print("FALLO: Se detectó mensaje de error")
                print(f"Mensaje de error: {error_message.text}")
                result = False
            except:
                # Verificar si el instructor aparece en la lista
                try:
                    instructor_list = driver.find_element(By.XPATH, "//*[contains(text(), 'Juan Pérez') or contains(text(), 'juan.perez@unsa.edu.pe')]")
                    print("ÉXITO: El instructor aparece registrado en la lista")
                    result = True
                except:
                    print("INCONCLUSO: No se detectó resultado claro")
                    result = "unknown"

        print("=== TEST CP-RF-0001-Q COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-Q", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()
            
if __name__ == "__main__":
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El registro por lotes fue exitoso")
    elif resultado == False:
        print("TEST FALLÓ: El registro por lotes falló")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
