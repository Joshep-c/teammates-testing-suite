"""
Funciones auxiliares comunes para todos los tests de TEAMMATES
"""
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_page_load(driver, timeout=10):
    """Espera a que la página cargue completamente"""
    try:
        # Esperar a que desaparezca el loading spinner
        wait = WebDriverWait(driver, timeout)
        wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "loading-container")))
        print("✓ Página cargada completamente")
        return True
    except:
        print("⚠ Loading spinner no encontrado o timeout")
        return False

def take_screenshot(driver, test_name, step="", img_dir="img"):
    """
    Toma screenshot con nombre estandarizado
    
    Args:
        driver: WebDriver instance
        test_name: Nombre del test (e.g., "CP-RF-0002-A")
        step: Paso del test (e.g., "initial", "final", "error")
        img_dir: Directorio donde guardar la imagen
    
    Returns:
        str: Ruta del archivo guardado
    """
    try:
        # Crear directorio si no existe
        caller_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(caller_dir, img_dir)
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generar nombre del archivo
        timestamp = int(time.time())
        step_suffix = f"-{step}" if step else ""
        filename = f"IMG-{timestamp}-{test_name}{step_suffix}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Tomar screenshot
        driver.save_screenshot(filepath)
        print(f"Screenshot guardado: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error tomando screenshot: {e}")
        return None

def find_and_click_button(driver, button_selectors, timeout=10):
    """
    Busca y hace clic en un botón usando múltiples selectores
    
    Args:
        driver: WebDriver instance
        button_selectors: Lista de tuplas (By.TYPE, "selector")
        timeout: Timeout en segundos
    
    Returns:
        bool: True si encontró y hizo clic en el botón
    """
    wait = WebDriverWait(driver, timeout)
    
    for selector_type, selector_value in button_selectors:
        try:
            button = wait.until(EC.element_to_be_clickable((selector_type, selector_value)))
            button.click()
            print(f"✓ Botón encontrado y clickeado: {selector_type} = '{selector_value}'")
            return True
        except:
            continue
    
    print("✗ No se pudo encontrar ningún botón con los selectores proporcionados")
    return False

def verify_form_fields(driver, field_ids):
    """
    Verifica que los campos del formulario estén presentes y visibles
    
    Args:
        driver: WebDriver instance
        field_ids: Lista de IDs de campos a verificar
    
    Returns:
        dict: Diccionario con el estado de cada campo
    """
    field_status = {}
    
    for field_id in field_ids:
        try:
            field = driver.find_element(By.ID, field_id)
            field_status[field_id] = {
                "found": True,
                "visible": field.is_displayed(),
                "enabled": field.is_enabled(),
                "type": field.get_attribute('type') or 'unknown'
            }
        except:
            field_status[field_id] = {
                "found": False,
                "visible": False,
                "enabled": False,
                "type": "unknown"
            }
    
    return field_status

def wait_and_find_element(driver, selector_type, selector_value, timeout=10):
    """
    Espera y encuentra un elemento con manejo de errores
    
    Args:
        driver: WebDriver instance
        selector_type: Tipo de selector (By.ID, By.XPATH, etc.)
        selector_value: Valor del selector
        timeout: Timeout en segundos
    
    Returns:
        WebElement or None: Elemento encontrado o None si no se encuentra
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
        return element
    except Exception as e:
        print(f"Error encontrando elemento {selector_type}='{selector_value}': {e}")
        return None

def clear_and_send_keys(driver, field_id, text):
    """
    Limpia un campo y envía texto con manejo de errores
    
    Args:
        driver: WebDriver instance
        field_id: ID del campo
        text: Texto a enviar
    
    Returns:
        bool: True si fue exitoso
    """
    try:
        field = driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(text)
        print(f"✓ Campo '{field_id}' llenado con: '{text}'")
        return True
    except Exception as e:
        print(f"✗ Error llenando campo '{field_id}': {e}")
        return False

def find_error_messages(driver):
    """
    Busca mensajes de error en la página usando múltiples selectores
    
    Args:
        driver: WebDriver instance
    
    Returns:
        list: Lista de mensajes de error encontrados
    """
    error_messages = []
    
    # Selectores comunes para mensajes de error
    error_selectors = [
        (By.CLASS_NAME, "text-danger"),
        (By.CLASS_NAME, "alert-danger"),
        (By.CLASS_NAME, "error"),
        (By.CLASS_NAME, "invalid-feedback"),
        (By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'invalid') or contains(@class, 'danger')]"),
        (By.XPATH, "//*[contains(text(), 'required') or contains(text(), 'cannot be empty') or contains(text(), 'field is required')]")
    ]
    
    for selector_type, selector_value in error_selectors:
        try:
            elements = driver.find_elements(selector_type, selector_value)
            for element in elements:
                text = element.text.strip()
                if text and text not in error_messages:
                    error_messages.append(text)
        except:
            continue
    
    return error_messages

def find_success_indicators(driver):
    """
    Busca indicadores de éxito en la página
    
    Args:
        driver: WebDriver instance
    
    Returns:
        list: Lista de indicadores de éxito encontrados
    """
    success_indicators = []
    
    # Selectores comunes para mensajes de éxito
    success_selectors = [
        (By.CLASS_NAME, "alert-success"),
        (By.CLASS_NAME, "text-success"),
        (By.CLASS_NAME, "success"),
        (By.XPATH, "//*[contains(@class, 'success')]"),
        (By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'added') or contains(text(), 'created')]")
    ]
    
    for selector_type, selector_value in success_selectors:
        try:
            elements = driver.find_elements(selector_type, selector_value)
            for element in elements:
                text = element.text.strip()
                if text and text not in success_indicators:
                    success_indicators.append(text)
        except:
            continue
    
    return success_indicators
