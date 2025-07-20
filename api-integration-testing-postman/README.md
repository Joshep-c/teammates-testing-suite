# Pruebas de Integración de API con Postman

Este módulo contiene pruebas de integración de la API REST de la plataforma **Teammates**, utilizando **Postman** y su CLI companion **Newman** para validar el comportamiento correcto de los endpoints.

## Contenido

- `Teammates.postman_collection.json`: Colección principal de pruebas automatizadas.
- `Teammates.postman_environment.json`: Entorno configurado con variables como URL base, tokens, etc.
- Reportes generados (CLI o HTML).
- Documentación interna sobre los casos cubiertos.

## Requisitos

- Postman Desktop App (opcional, para ejecutar y editar)
- Node.js (para ejecutar Newman)
- Newman (CLI para ejecución automatizada)
   ```bash
   npm install -g newman

## Ejecución

Para su ejecución consideramos que se cumple los requisitos anteriores por lo que usaremos una terminal para ejecutar las pruebas presentes
   ```bash
   newman run TEAMMATES_Complete_Collection.postman_collection.json -e TEAMMATES_Environment.postman_environment.json
