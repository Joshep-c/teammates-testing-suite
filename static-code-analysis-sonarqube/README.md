# Resumen del Análisis Estático de Código – TEAMMATES

## 1. Contexto
Se analizó el repositorio de **TEAMMATES** con **SonarCloud** para medir calidad de código (seguridad, confiabilidad y mantenibilidad), deuda técnica y cobertura de pruebas.  
El primer escaneo global (~3 915 issues, 63 días-persona de deuda) mezclaba backend, frontend y carpetas de prueba, así que se **separó el análisis por componentes**.

## 2. Separación de proyectos
- **Backend limpio**: `teammates-backend-clean` (solo `src/main/java`, excluyendo e2e/it/web/resources).  
- **Frontend limpio**: `teammates-frontend-clean` (solo `src/web`, excluyendo specs, helpers y configs).

## 3. Cobertura y análisis

### Backend (Java – Gradle + JaCoCo)
1. Ejecutar pruebas unitarias: `./gradlew unitTests` (genera `build/jacoco/unitTests.exec`).  
2. Generar reporte XML sin re‑ejecutar tests: `./gradlew jacocoTestReport --continue`  
   - Salida: `build/reports/jacoco/test/jacocoTestReport.xml`.  
3. Configurar `sonar-project.properties` apuntando a fuentes, exclusiones y `sonar.coverage.jacoco.xmlReportPaths`.  
4. Lanzar SonarScanner: `sonar-scanner -Dsonar.token=<TOKEN>`.

**Resultado clave**  
- 16 bugs, 1 279 code smells, 2 hotspots de seguridad.  
- Cobertura: ~30 %.  
- Quality Gate: **PASSED**.

### Frontend (Angular – Jest/Karma + Istanbul)
1. Generar tipos compartidos: `./gradlew generateTypes`  
   - `src/web/types/api-output.ts` y `src/web/types/api-request.ts`.  
2. Ejecutar cobertura: `npm run coverage`  
   - Salida: `coverage/lcov.info`.  
3. Configurar `sonar-project.properties` (inclusiones TS/HTML/SCSS, exclusiones de tests) y `sonar.javascript.lcov.reportPaths=coverage/lcov.info`.  
4. Subir con SonarScanner.

**Resultado clave**  
- 142 bugs, 12 code smells, 4 hotspots (XSS/DoS).  
- Cobertura: ~65 %.  
- Quality Gate: **PASSED**.

## 4. Reportes y evidencias

### Plugin Bitegarden (PDF/Excel)
Se generaron reportes ejecutivos con:
```bash
java -Dsonar.token=... -Dsonar.projectKey=... -Dreport.type=<2|3|6|7|9>      -Doutput=<archivo.pdf/xlsx> -jar bitegarden-sonarcloud-report-1.8.1.jar
```

### API SonarCloud (PowerShell)
Scripts para descargar métricas, issues y hotspots en **CSV/JSON**:
- `/api/measures/component` → métricas globales.  
- `/api/issues/search` → bugs, vulnerabilidades, code smells.  
- `/api/hotspots/search` → security hotspots.

## 5. Hallazgos principales
- La mayoría de problemas son **code smells** (duplicación de literales, alta complejidad, dependencias circulares – Java; funciones complejas y `sort` sin comparador – TS).  
- No hay issues bloqueantes ni vulnerabilidades confirmadas, pero **hay hotspots por revisar**.  
- Cobertura aceptable en frontend, baja en backend: priorizar módulos críticos.  
- Quality Gate aprobado en ambos componentes, pero con **ratings D** en fiabilidad/seguridad que requieren atención.

## 6. Recomendaciones rápidas
1. **Corregir primero** bugs críticos, vulnerabilidades y revisar hotspots.  
2. **Subir cobertura** en código nuevo (≥80 %) y reforzar módulos con alta deuda/baja cobertura.  
3. **Refactorizar** métodos complejos, eliminar duplicaciones y dependencias circulares.  
4. **Automatizar** generación de reportes (Bitegarden + API) en el pipeline CI/CD.  
5. Mantener un **ciclo de mejora continua**: reducir deuda ≥5 % por sprint y revisar métricas en cada PR.

---
_Elaborado por: Congona Manrique, M. E. & Delgado Allpan, A. D. (Julio 2025)_
