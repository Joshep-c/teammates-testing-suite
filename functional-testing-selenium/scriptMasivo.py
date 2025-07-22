#!/usr/bin/env python3
"""
Script Masivo para Cambiar Nomenclatura de Screenshots
Actualiza todos los casos de prueba para usar nombres descriptivos en capturas de pantalla
Patrón: CP-RF-XXXX-X-entrada.png, CP-RF-XXXX-X-salida.png
"""

import os
import re
import glob

def extract_test_case_name(file_path):
    """
    Extrae el nombre del caso de prueba del archivo
    Ej: CP-RF-0001-A.py -> CP-RF-0001-A
    """
    filename = os.path.basename(file_path)
    # Extraer el patrón CP-RF-XXXX-X
    match = re.search(r'(CP-RF-\d{4}-[A-Z])', filename)
    if match:
        return match.group(1)
    return None

def update_screenshot_names_in_file(file_path):
    """
    Actualiza los nombres de screenshots en un archivo de prueba
    """
    try:
        # Leer el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer el nombre del caso de prueba
        test_case_name = extract_test_case_name(file_path)
        if not test_case_name:
            print(f"⚠ No se pudo extraer nombre del caso de prueba: {file_path}")
            return False
        
        # Contador de cambios
        changes_made = 0
        
        # PATRÓN 1: Función take_screenshot (usado en RF-0001)
        # Cambiar "initial" por "entrada"
        pattern_initial = rf'take_screenshot\(driver,\s*"{re.escape(test_case_name)}",\s*"initial"\)'
        replacement_initial = f'take_screenshot(driver, "{test_case_name}", "entrada")'
        if re.search(pattern_initial, content):
            content = re.sub(pattern_initial, replacement_initial, content)
            changes_made += 1
            print(f"✓ Actualizado take_screenshot initial -> entrada en {test_case_name}")
        
        # Cambiar "final" por "salida"
        pattern_final = rf'take_screenshot\(driver,\s*"{re.escape(test_case_name)}",\s*"final"\)'
        replacement_final = f'take_screenshot(driver, "{test_case_name}", "salida")'
        if re.search(pattern_final, content):
            content = re.sub(pattern_final, replacement_final, content)
            changes_made += 1
            print(f"✓ Actualizado take_screenshot final -> salida en {test_case_name}")
        
        # PATRÓN 2: os.path.join con IMG- (usado en RF-0002 y otros)
        # 1. Screenshot inicial -> entrada
        patterns_entrada = [
            (r'screenshot_path\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-1-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-entrada.png")'),
            (r'screenshot_path\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-INICIAL-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-entrada.png")'),
        ]
        
        for pattern, replacement in patterns_entrada:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made += 1
                print(f"✓ Actualizado screenshot inicial -> entrada en {test_case_name}")
        
        # 2. Screenshot final -> salida
        patterns_salida = [
            (r'screenshot_path_final\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-FINAL-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path_final = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-salida.png")'),
            (r'screenshot_path_final\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-END-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path_final = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-salida.png")'),
        ]
        
        for pattern, replacement in patterns_salida:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made += 1
                print(f"✓ Actualizado screenshot final -> salida en {test_case_name}")
        
        # 3. Screenshots intermedios -> descriptivos
        patterns_intermedios = [
            # Screenshot después de llenar campos
            (r'screenshot_path_2\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-2-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path_2 = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-campos-llenados.png")'),
            # Screenshot de debug
            (r'screenshot_path_3\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-3-' + re.escape(test_case_name) + r'-debug\.png"\)',
             f'screenshot_path_3 = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-debug.png")'),
            # Screenshot de error
            (r'screenshot_path_error\s*=\s*os\.path\.join\([^)]+,\s*"img",\s*"IMG-ERROR-' + re.escape(test_case_name) + r'\.png"\)',
             f'screenshot_path_error = os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-error.png")'),
        ]
        
        for pattern, replacement in patterns_intermedios:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made += 1
                print(f"✓ Actualizado screenshot intermedio en {test_case_name}")
        
        # 4. Patrones genéricos para cualquier IMG- que se haya perdido
        generic_patterns = [
            # Cualquier IMG-número-TESTCASE.png
            (r'os\.path\.join\([^)]+,\s*"img",\s*"IMG-\d+-' + re.escape(test_case_name) + r'\.png"\)',
             f'os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-captura.png")'),
            # Cualquier IMG-TEXTO-TESTCASE.png
            (r'os\.path\.join\([^)]+,\s*"img",\s*"IMG-[A-Z]+-' + re.escape(test_case_name) + r'\.png"\)',
             f'os.path.join(os.path.dirname(__file__), "img", "{test_case_name}-captura.png")'),
        ]
        
        for pattern, replacement in generic_patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_made += len(matches)
                print(f"✓ Actualizado {len(matches)} screenshot(s) genérico(s) en {test_case_name}")
        
        # Escribir el archivo actualizado si hubo cambios
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Archivo actualizado: {file_path} ({changes_made} cambios)")
            return True
        else:
            print(f"📄 Sin cambios necesarios: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando {file_path}: {e}")
        return False

def find_python_test_files(base_path):
    """
    Encuentra todos los archivos de prueba Python en las carpetas RF-*
    """
    test_files = []
    
    # Buscar en todas las carpetas RF-*
    rf_pattern = os.path.join(base_path, "tests", "RF-*")
    rf_folders = glob.glob(rf_pattern)
    
    for rf_folder in rf_folders:
        if os.path.isdir(rf_folder):
            # Buscar archivos CP-*.py directamente en la carpeta RF
            cp_pattern = os.path.join(rf_folder, "CP-*.py")
            cp_files = glob.glob(cp_pattern)
            test_files.extend(cp_files)
            
            # Buscar archivos CP-*.py en subcarpetas
            subfolders_pattern = os.path.join(rf_folder, "CP-*")
            subfolders = glob.glob(subfolders_pattern)
            
            for subfolder in subfolders:
                if os.path.isdir(subfolder):
                    py_files = glob.glob(os.path.join(subfolder, "*.py"))
                    test_files.extend(py_files)
    
    return test_files

def main():
    """
    Función principal que ejecuta el script masivo
    """
    print("="*60)
    print("🔄 SCRIPT MASIVO: ACTUALIZACIÓN DE NOMENCLATURA DE SCREENSHOTS")
    print("="*60)
    print("Objetivo: Cambiar nombres de capturas por esquema descriptivo")
    print("Patrón: CP-RF-XXXX-X-entrada.png, CP-RF-XXXX-X-salida.png")
    print("")
    
    # Obtener el directorio base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = script_dir
    
    print(f"📁 Directorio base: {base_path}")
    print("")
    
    # Encontrar archivos de prueba
    print("🔍 Buscando archivos de prueba...")
    test_files = find_python_test_files(base_path)
    
    if not test_files:
        print("❌ No se encontraron archivos de prueba Python")
        return
    
    print(f"✓ Encontrados {len(test_files)} archivos de prueba")
    print("")
    
    # Mostrar archivos encontrados
    print("📋 Archivos a procesar:")
    for i, file_path in enumerate(test_files, 1):
        rel_path = os.path.relpath(file_path, base_path)
        print(f"  {i:2d}. {rel_path}")
    print("")
    
    # Confirmar ejecución
    try:
        response = input("¿Continuar con la actualización? (s/n): ").lower().strip()
        if response not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada por el usuario")
            return
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
        return
    
    print("")
    print("🚀 Iniciando actualización masiva...")
    print("-" * 40)
    
    # Procesar archivos
    total_files = len(test_files)
    updated_files = 0
    
    for i, file_path in enumerate(test_files, 1):
        rel_path = os.path.relpath(file_path, base_path)
        print(f"\n[{i}/{total_files}] Procesando: {rel_path}")
        
        if update_screenshot_names_in_file(file_path):
            updated_files += 1
    
    # Resumen final
    print("")
    print("="*60)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("="*60)
    print(f"Total de archivos procesados: {total_files}")
    print(f"Archivos actualizados: {updated_files}")
    print(f"Archivos sin cambios: {total_files - updated_files}")
    print("")
    
    if updated_files > 0:
        print("✅ Actualización completada exitosamente!")
        print("")
        print("🎯 Nuevo esquema de nomenclatura aplicado:")
        print("  • CP-RF-XXXX-X-entrada.png (screenshot inicial)")
        print("  • CP-RF-XXXX-X-salida.png (screenshot final)")
        print("  • CP-RF-XXXX-X-campos-llenados.png (después de llenar)")
        print("  • CP-RF-XXXX-X-debug.png (para análisis)")
        print("  • CP-RF-XXXX-X-error.png (capturas de error)")
    else:
        print("ℹ️ No se realizaron cambios en los archivos")
    
    print("")

if __name__ == "__main__":
    main()
