"""
Driver Setup Global para todos los tests de TEAMMATES
Maneja la configuración unificada de Selenium WebDriver con gestión de cookies
"""
import subprocess
import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración global
CHROME_PROFILE_PATH = "C:/temp/selenium_chrome"
CHROME_DEBUG_PORT = 9225
COOKIES_BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'cookies')

def close_all_chrome():
    """Cierra todos los procesos de Chrome de forma agresiva"""
    try:
        # Cerrar Chrome normalmente
        subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], 
                      capture_output=True, text=True, check=False)
        time.sleep(2)
        
        # Cerrar procesos relacionados
        subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe"], 
                      capture_output=True, text=True, check=False)
        time.sleep(1)
        
    except Exception as e:
        print(f"Error cerrando Chrome: {e}")

def load_cookies(driver, cookie_type="general"):
    """
    Carga cookies guardadas
    
    Args:
        driver: Instancia de WebDriver
        cookie_type: Tipo de cookies a cargar ("general", "instructor", "student")
    
    Returns:
        bool: True si las cookies se cargaron exitosamente
    """
    try:
        # Definir rutas de cookies por tipo
        cookie_files = {
            "general": "cookies.pkl",
            "instructor": "instructor_cookies.pkl", 
            "student": "student_cookies.pkl"
        }
        
        # Intentar cargar cookies en orden de prioridad
        cookie_priorities = []
        if cookie_type in cookie_files:
            cookie_priorities.append((cookie_files[cookie_type], cookie_type))
        
        # Agregar cookies generales como respaldo
        if cookie_type != "general":
            cookie_priorities.append((cookie_files["general"], "general"))
        
        cookies_loaded = False
        
        for cookie_file, source in cookie_priorities:
            cookie_path = os.path.join(COOKIES_BASE_PATH, cookie_file)
            
            if os.path.exists(cookie_path):
                try:
                    with open(cookie_path, 'rb') as f:
                        cookies_data = pickle.load(f)
                    
                    # Navegar a la página base para establecer el dominio
                    driver.get("https://modern-vortex-463217-h9.appspot.com")
                    
                    # Cargar las cookies
                    loaded_count = 0
                    for cookie in cookies_data:
                        try:
                            driver.add_cookie(cookie)
                            loaded_count += 1
                        except Exception as e:
                            print(f"Error cargando cookie individual: {e}")
                    
                    print(f"Cookies {source} cargadas: {loaded_count}/{len(cookies_data)} cookies")
                    cookies_loaded = True
                    break
                    
                except Exception as e:
                    print(f"Error leyendo archivo de cookies {source}: {e}")
                    continue
        
        if not cookies_loaded:
            print(f"No se encontraron cookies válidas para tipo '{cookie_type}'")
            
        return cookies_loaded
        
    except Exception as e:
        print(f"Error en load_cookies: {e}")
        return False

def save_cookies(driver, cookie_type="general"):
    """
    Guarda las cookies actuales del navegador
    
    Args:
        driver: Instancia de WebDriver
        cookie_type: Tipo de cookies a guardar ("general", "instructor", "student")
    
    Returns:
        bool: True si las cookies se guardaron exitosamente
    """
    try:
        cookie_files = {
            "general": "cookies.pkl",
            "instructor": "instructor_cookies.pkl",
            "student": "student_cookies.pkl"
        }
        
        if cookie_type not in cookie_files:
            print(f"Tipo de cookie no válido: {cookie_type}")
            return False
        
        # Crear directorio si no existe
        os.makedirs(COOKIES_BASE_PATH, exist_ok=True)
        
        # Obtener cookies actuales
        cookies = driver.get_cookies()
        
        # Guardar cookies
        cookie_path = os.path.join(COOKIES_BASE_PATH, cookie_files[cookie_type])
        with open(cookie_path, 'wb') as f:
            pickle.dump(cookies, f)
        
        print(f"Cookies {cookie_type} guardadas: {len(cookies)} cookies en {cookie_path}")
        return True
        
    except Exception as e:
        print(f"Error guardando cookies: {e}")
        return False

def get_driver(use_saved_session=True, cookie_type="general", debug_port=None):
    """
    Crea una instancia de WebDriver con configuración optimizada
    
    Args:
        use_saved_session: Si cargar cookies guardadas
        cookie_type: Tipo de cookies a cargar ("general", "instructor", "student")
        debug_port: Puerto de debug de Chrome (None para usar default)
    
    Returns:
        WebDriver: Instancia configurada del navegador
    """
    # Cerrar Chrome antes de crear nueva instancia
    close_all_chrome()
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Puerto de debug
    port = debug_port if debug_port else CHROME_DEBUG_PORT
    chrome_options.add_argument(f"--remote-debugging-port={port}")
    
    # Evitar detección de automatización
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Crear driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    driver.maximize_window()
    
    # Script para evitar detección
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    """ 
    # Cargar cookies si está habilitado
    if use_saved_session:
        if load_cookies(driver, cookie_type):
            print(f"Sesión {cookie_type} restaurada desde cookies")
        else:
            print("No se pudo restaurar sesión, se requerirá login manual")
    """
    return driver

def get_driver_for_rf(rf_number, use_saved_session=True):
    """
    Método de conveniencia para obtener driver específico por RF
    
    Args:
        rf_number: Número del RF (e.g., "0001", "0002")
        use_saved_session: Si cargar cookies guardadas
    
    Returns:
        WebDriver: Instancia configurada del navegador
    """
    # Mapeo de RF a tipos de cookie y puertos
    rf_config = {
        "0001": {"cookie_type": "general", "debug_port": 9225},
        "0002": {"cookie_type": "instructor", "debug_port": 9226},
        # Agregar más RFs según necesidad
    }
    
    config = rf_config.get(rf_number, {"cookie_type": "general", "debug_port": 9225})
    
    return get_driver(
        use_saved_session=use_saved_session,
        cookie_type=config["cookie_type"],
        debug_port=config["debug_port"]
    )
