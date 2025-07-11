# Análisis Estático de Código con SonarQube

Este módulo realiza un análisis estático del código fuente de la plataforma **Teammates** utilizando **SonarQube**.

## Contenido

- `sonar-project.properties`: Configuración para ejecutar el análisis con SonarScanner.
- Reportes exportados de SonarQube.
- Capturas de pantalla y métricas de calidad del código.

## Requisitos

- Java 11 o superior
- SonarScanner CLI
- Un servidor SonarQube (local o remoto)

## Instrucciones

1. Instala SonarScanner:  
   [Guía oficial](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/)

2. Ejecuta el análisis:
   ```bash
   sonar-scanner
