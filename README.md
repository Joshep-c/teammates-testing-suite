# teammates-testing-suite

Este repositorio contiene una colección de pruebas y análisis automatizados realizados sobre la plataforma **Teammates**, con el objetivo de evaluar su calidad, rendimiento y robustez.

## Estructura del Proyecto

### `/static-code-analysis-sonarqube`
Contiene el análisis estático del código fuente de Teammates utilizando **SonarQube**.  
Incluye:
- Configuración de `sonar-project.properties`
- Capturas de resultados de análisis
- Reportes de calidad del código (bugs, code smells, duplicaciones, etc.)

### `/performance-testing-k6`
Incluye pruebas de rendimiento usando **K6**.  
Se enfocan en:
- Carga concurrente de usuarios
- Pruebas de estrés
- Reportes de tiempo de respuesta y rendimiento del servidor

### `/functional-testing-selenium`
Automatización de pruebas funcionales con **Selenium**, cubriendo al menos el 50% de los casos principales.  
Contiene:
- Scripts de prueba para UI
- Evidencia de ejecución
- Instrucciones para correr las pruebas

### `/api-integration-testing-postman`
Colecciones y entornos de **Postman** para pruebas de integración sobre las APIs REST expuestas por Teammates.  
Incluye:
- Pruebas de endpoints
- Validación de respuestas
- Pruebas de seguridad básica

---

## Requisitos

- Node.js y npm (para K6)
- Java 11+ (para SonarScanner)
- Selenium WebDriver (Python/JavaScript)
- Postman o Newman (para ejecutar pruebas desde CLI)

## Cómo ejecutar las pruebas

Cada carpeta contiene su propio `README.md` con instrucciones específicas para ejecutar las pruebas correspondientes.

---

## Autores

- Ccahuana Larota Joshep Antony
- Cordova Sellerico James Seus
- Condorios Yllapuma Jorge Enrique
- Carrasco Choque Arles Melvin
- Huamaní Vargas Melsy Melany
- Huisa Perez Willy Alexander 
- Roque Quispe William Isaias
- Congona Manrique Mauricio Elías

- Universidad Nacional de San Agustin

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
