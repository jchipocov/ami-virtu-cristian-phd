# Agenda de Análisis Estadístico y Modelamiento (Día 2)

## Estado Actual 
✅ **Arquitectura Computacional:** Finalizada y Auditada.
✅ **Ingeniería de Características (Features):** Estandarizada contra Data Leakage.
✅ **Simulación Restringida:** Validaciones psicométricas forzadas mediante Cópulas Gaussianas y Pruebas Unitarias Pytest al 100%.

---

## Objetivo Central para Mañana (¡CUMPLIDO!)
Se ha realizado con éxito la transición del ámbito de "Ingeniería de Datos" hacia la **"Inferencia Científica y Educativa"**.

### Fase 1: Disección Predictiva (Supervisada) - ✅ COMPLETADO
- [x] **Extraer la "Radiografía del Peligro" (Logit):** Implementado el cálculo automático de **Odds Ratios ($Exp(\beta)$)** con interpretación lingüística del riesgo.
- [x] Optimización de Clasificación (Índice de Youden)
- [x] Implementación de Modelos de Ensamble (Gradient Boosting)
- [x] Validación Cruzada (CV=5) y Tuning de Hiperparámetros
- [x] **Fase 6 [XAI]:** Explicabilidad total con SHAP (Logit y GB)
- [x] Automatización de Bitácora de Ejecución Científica
- [x] **Evaluación de Precision vs Recall (KNN):** Integración de **Matrices de Confusión** en el Dashboard para auditar la performance y detectar Falsos Negativos.
- [x] **Modelamiento de Interacción (La AMI como Amplificador):** Formalizada y testeada la hipótesis $Riesgo \sim AMI + Calidad + (AMI \times Calidad)$. El pipeline reporta significancia estadística del efecto moderador.

### Fase 2: Perfilamiento Sociológico Estudiantil (No Supervisado) - ✅ COMPLETADO
- [x] **Bautizo de Centroides (K-Means y GMM):** Implementado el sistema de **Radar Charts** para visualizar el "ADN" de cada clúster. Los perfiles están listos para ser nombrados cualitativamente.
- [x] **El "Juicio" de DBSCAN:** Motor de detección de anomalías (Ruido -1) plenamente operativo para identificar casos atípicos.

### Fase 3: Trazado del Reemplazo "Raw Data" - ✅ COMPLETADO
- [x] **Simulacro Teórico del Intercambio:** Documentada la estructura de `real_data.csv` y creado el `template_real_data.csv`. El sistema es **Plug & Play** mediante el selector de entorno `APP_ENV`.
- [x] **Limpieza Post-Recolección:** Lógica de `DataCleaner` preparada para detectar inconsistencias y flatliners en datos reales.

---

## Fase 5: Blindaje Metodológico Doctoral (Rigor PhD) 🚀
*Esta sección integra las observaciones críticas para elevar el análisis a nivel de defensa de tesis y publicación Q1.*

*   [x] **Validación Estructural (EFA/CFA):** Ejecutar Análisis Factorial Exploratorio para validar la carga de ítems en las 3 dimensiones AMI (Crítica, Técnica, Participativa).
    *   Incluir pruebas de adecuación muestral: **KMO** (Kaiser-Meyer-Olkin) y **Prueba de Esfericidad de Bartlett**.
    *   Método de extracción: Máxima Verosimilitud (ML) o Ejes Principales.
    *   Rotación: Oblicua (**Oblimin** o Promax) para permitir correlación entre dimensiones.
*   [x] **Diagnósticos de Regresión:**
    *   Implementar cálculo de **VIF (Factor de Inflación de la Varianza)** para descartar multicolinealidad.
    *   Añadir pruebas de bondad de ajuste (**Hosmer-Lemeshow** y **Pseudo R² de McFadden**).
*   [x] **Justificación de Escalas:** Redactar en el informe la asunción de "categorías equidistantes" para el tratamiento de Likert como variable continua.
*   [x] **Refinamiento de Interacciones:** Documentar el proceso de **Mean-Centering** (centrado de medias) antes de construir los términos de interacción para estabilizar el modelo.
*   [x] **Rigor NLP:** Especificar el uso de modelos Transformer (Gemini-Flash) y métricas de validación cualitativa (Triangulación de Coherencia) para el análisis de sentimiento.
*   [x] **Blindaje XAI:** Explicitar que SHAP es una capa de interpretabilidad post-hoc y no una sustitución de la inferencia estadística tradicional.
*   [x] **Validación de Clustering:** Consolidar el uso de Silhouette Scores y BIC como criterios de estabilidad, reportando el consenso entre modelos (K-Means vs GMM).
*   [x] **Desglose Dimensional del Riesgo (Alineación Objetivos 2 y 3):** ✅ FINALIZADO
    *   **Objetivo 2:** Separar la variable dependiente `Riesgo` en sus 3 dimensiones originales: **Académica**, **Comportamiento LMS** y **Continuidad**. (Implementado en `scorer.py`)
    *   **Objetivo 3:** Utilizar estos desgloses para caracterizar los perfiles (clusters). Identificado perfil predominantemente tecnológico (LMS) vs académico.
    *   **Psicometría ARD-VIRTU:** Calculado Alfa (0.96) y Omega (0.98) para la sub-escala de riesgo LMS, validando el instrumento.
    *   **Análisis Bivariado:** Generada la matriz de correlación cruzada (3x3) entre AMI y dimensiones de Riesgo.
*   [x] **Reproducibilidad Científica:** Asegurar el uso de semillas fijas (`random_state`), versionado de datos mediante **SHA-256** y auditoría de entorno (`VerifyEnv`).

---
*Última actualización de ruta: 28 de Abril de 2026 (Ajuste post-revisión de rigor).*

## Fase 4: Seguridad y Privacidad (Hardening) - ✅ COMPLETADO
*   [x] **Filtro PII Automático**: Implementar capa en `DataCleaner` para eliminar columnas sensibles (DNI, Nombres, Correo) antes del análisis.
*   [x] **Validación de Rutas**: Asegurar que el cargador de datos no permita accesos fuera del directorio `data/`.
*   [x] **Sanitización de Logs**: Verificar que el volcado detallado de la bitácora no contenga muestras de datos brutos (raw data).
*   [x] **Auditoría de Dependencias**: Verificado manualmente el uso de librerías seguras.
