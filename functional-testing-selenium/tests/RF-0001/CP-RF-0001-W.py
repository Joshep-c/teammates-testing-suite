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
    CP-RF-0001-W: Registro masivo mixto: líneas válidas e inválidas
    RF-0001: Tabla de Decisiones
    Verificar que, al procesar un lote con algunas líneas válidas y otras inválidas, 
    solo las válidas se registren y se informe error de las inválidas
    """
    print("=== INICIANDO TEST CP-RF-0001-W ===")
    print("Objetivo: Registro masivo mixto con líneas válidas e inválidas")
    print("Datos de prueba:")
    print("  Línea válida: Antony|antony.perez@unsa.edu.pe|UNSA")
    print("  Línea inválida: Invalid|noatsignunsa.edu.pe|")
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
        
        # Limpiar y llenar el campo de registro por lotes con datos mixtos
        batch_data = """Antony|antony.perez@unsa.edu.pe|UNSA
Invalid|noatsignunsa.edu.pe|"""
        print("Llenando campo de registro por lotes con datos mixtos...")
        print("  Línea válida: Antony|antony.perez@unsa.edu.pe|UNSA")
        print("  Línea inválida: Invalid|noatsignunsa.edu.pe|")
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
        print(f"  Líneas de registro: {len(batch_data.split(chr(10)))} líneas")

        # IMAGEN 1: Captura después de llenar los datos mixtos
        time.sleep(2)

        # Hacer clic en "Add Instructors"
        add_batch_button.click()

        time.sleep(3)
        
        # Desplazar al final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # IMAGEN 2: Captura después de hacer clic en "Add Instructors"
        time.sleep(2)  # Esperar un poco para que se procese la acción

        # Verificar el resultado del registro mixto
        print("Verificando resultado del registro masivo mixto...")
        
        valid_registered = False
        invalid_rejected = False
        
        try:
            # Verificar si Antony fue registrado exitosamente
            antony_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Antony') or contains(text(), 'antony.perez@unsa.edu.pe')]")
            print("ÉXITO: Antony fue registrado correctamente")
            valid_registered = True
        except:
            print("FALLO: Antony no fue registrado")
        
        try:
            # Buscar mensajes de error para líneas inválidas
            error_messages = driver.find_elements(By.CLASS_NAME, "alert-danger")
            warning_messages = driver.find_elements(By.CLASS_NAME, "alert-warning")
            
            if error_messages or warning_messages:
                print("ÉXITO: Se detectaron mensajes de error/advertencia para líneas inválidas")
                for msg in error_messages + warning_messages:
                    print(f"  Mensaje: {msg.text}")
                invalid_rejected = True
            else:
                # Buscar texto que indique error en líneas específicas
                error_text = driver.find_element(By.XPATH, "//*[contains(text(), 'invalid') or contains(text(), 'error') or contains(text(), 'Invalid')]")
                print(f"ÉXITO: Se detectó indicación de error: {error_text.text}")
                invalid_rejected = True
        except:
            print("ADVERTENCIA: No se detectaron mensajes de error claros para líneas inválidas")
        
        # Evaluar resultado final
        if valid_registered and invalid_rejected:
            result = True
            print("ÉXITO COMPLETO: Líneas válidas registradas e inválidas rechazadas")
        elif valid_registered:
            result = "partial"
            print("ÉXITO PARCIAL: Líneas válidas registradas, pero no se detectó rechazo de inválidas")
        else:
            result = False
            print("FALLO: No se registraron las líneas válidas correctamente")

        print("=== TEST CP-RF-0001-W COMPLETADO ===")
        return result
        
    except Exception as e:
        print(f"ERROR durante la ejecución del test: {e}")
        if 'driver' in locals():        return False

    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        if 'driver' in locals():
            take_screenshot(driver, "CP-RF-0001-W", "error")
        return f"TEST FALLIDO: {e}"
    
    finally:
        # Cerrar el navegador
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    resultado = test_registro_instructor()
    if resultado == True:
        print("TEST PASÓ: El registro masivo mixto funcionó correctamente")
    elif resultado == "partial":
        print("TEST PARCIAL: Líneas válidas registradas, verificar manejo de inválidas")
    elif resultado == False:
        print("TEST FALLÓ: El registro masivo mixto no funcionó correctamente")
    else:
        print("TEST INCONCLUSO: No se pudo determinar el resultado")
