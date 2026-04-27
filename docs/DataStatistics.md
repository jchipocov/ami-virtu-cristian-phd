# Planificación Estadística y Pipeline de Datos (Versión Doctoral Extendida)

Este documento detalla de forma exhaustiva la estrategia estadística del software AMI-VIRTU. Ha sido actualizado para reflejar la transición de la fase de simulación a la fase de **Análisis de Campo Consolidada (N=295)**, integrando todos los hallazgos de las Fases 1 a 13 del proyecto.

---

## 1. Estrategia de Muestreo y Validación de la Cohorte

### 1.1. Tamaño Muestral (`N`) y Representatividad
- **Meta inicial:** 240 a 300 encuestas.
- **N Final Consolidado:** **295 estudiantes**. Esta cifra garantiza un poder estadístico robusto para el modelamiento inferencial, superando los umbrales mínimos requeridos para la estabilidad de la Regresión Logística y el Clustering Multivariado.
- **Proporción de Clases:** Se ha logrado identificar una proporción de riesgo que permite el entrenamiento equilibrado de modelos predictivos, evitando el sobreajuste (overfitting) y garantizando la generalización de los resultados a otras universidades públicas.

### 1.2. Transición de Datos Simulados a Reales
El simulador original utilizó **Cópulas Gaussianas Multivariadas** para inyectar un Modelo de Factor Latente, preservando las correlaciones entre AMI y Riesgo. Tras la recolección de los **295 casos reales**, el pipeline ha validado que las tendencias teóricas se mantienen: la Alfabetización Mediática (especialmente la técnica) actúa como el principal factor de protección contra la deserción virtual.

---

## 2. Definición y Preprocesamiento Profundo de Variables

### 2.1. Alfabetización Mediática (AMI-VIRTU)
El cuestionario principal (AMI-VIRTU) se compone de 30 ítems organizados en tres dimensiones fundamentales:
- **Dimensión Crítica:** 10 ítems (`C1 - C10`). Evalúa la capacidad de discernimiento y verificación de fuentes.
- **Dimensión Técnica:** 10 ítems (`T1 - T10`). Evalúa el dominio operativo de herramientas digitales y LMS.
- **Dimensión Participativa:** 10 ítems (`P1 - P10`). Evalúa la ética y frecuencia de la interacción en redes académicas.

#### A. Transformación Likert y Control de Calidad
Todas las respuestas se mapean de una escala ordinal de 5 puntos a valores numéricos continuos:
- **Totalmente en desacuerdo (1) -> Totalmente de acuerdo (5)**.

#### B. Inversión Semántica de Ítems de Control
Para neutralizar el *sesgo de aquiescencia*, se aplica la función de inversión $6 - x$ específicamente sobre:
- **C6:** Compartir información sin comprobar.
- **T6:** Evitar nuevas herramientas digitales.
- **P5:** Evitar compartir borradores o ayudas.
Esta técnica garantiza que un puntaje AMI alto represente consistentemente una mayor competencia, incluso en preguntas redactadas en sentido negativo.

### 2.2. Matriz de Riesgo de Deserción (ARD-VIRTU)
El constructo "Riesgo de Deserción" se operacionaliza como una variable dicotómica ($Y=1$ o $Y=0$).

#### A. Algoritmo de Cálculo de Riesgo Total
El sistema activa el riesgo ($Y=1$) si el estudiante cumple cualquier criterio de la siguiente compuerta lógica `OR`:
1.  **Interrupción Académica (`A1`):** El alumno reconoce haber detenido sus estudios anteriormente.
2.  **Reprobación Sostenida (`A2`):** Haber desaprobado dos o más cursos en el ciclo vigente.
3.  **Retiros Administrativos (`A3`):** Haberse retirado de una o más asignaturas.
4.  **Inactividad Crítica (`L2`):** Reportar inactividad en el entorno virtual superior a 15 días.

#### B. El Detector de Inconsistencia y Ocultamiento
El módulo `DataCleaner` integra un **Detector de Inconsistencias** que genera una bandera estadística (`Flag_Inconsistencia = True`) sobre casos que mienten o responden al azar (ej. marcan 5 en todos los ítems AMI, ignorando los invertidos). En los modelos finales, estos registros son penalizados o excluidos mediante el **Filtro de Coherencia Agresivo (Indice < 0.6)**, asegurando que la tesis trabaje solo con "data limpia".

---

## 3. Plan Analítico Doctoral Multi-Fase

### Fase 1: Análisis Psicométrico de Consistencia
Se emplean estimadores de alta precisión para validar que el instrumento mide lo que dice medir:
- **Alfa de Cronbach ($\alpha$):** Consistencia interna clásica.
- **Omega de McDonald ($\omega$):** Estimador jerárquico que no asume tau-equivalencia, siendo el standard actual de oro en psicometría avanzada.

### Fase 2: Inferencia Predictiva y Regresión Logística
Se utiliza el método de **Máxima Verosimilitud (MLE)** en `statsmodels` para:
- **Calcular Odds Ratios (OR):** Magnitud en la que cada punto AMI reduce el riesgo.
- **P-valores:** Determinación de la significancia estadística ($p < .05$).
- **Efectos de Interacción:** Validación de la hipótesis de que la AMI es un moderador entre la calidad del sistema y la retención.

### Fase 3: Inteligencia Artificial Explicable (XAI)
Uso de **KernelSHAP** para romper con el modelo de "caja negra":
- Se extrae un ranking de los 30 ítems individuales según su impacto real en el riesgo.
- Se identifican "Ítems Críticos" para la intervención pedagógica inmediata.

### Fase 4: Triangulación de Métodos Mixtos (Novedad Doctoral)
Se implementa una integración cuali-cuanti:
- **NLP de Sentimientos:** Procesamiento de las respuestas de la `Section B`.
- **Cruce de Disonancia:** Identificación de alumnos con alto AMI pero bajo sentimiento, permitiendo una detección proactiva de fatiga académica (burnout).

### Fase 5: Ensamble de Clustering para Perfilamiento
Segmentación mediante 4 algoritmos concurrentes para asegurar la estabilidad: **K-Means, Ward, DBSCAN y GMM**. Esto define los 3 arquetipos: **Competente, Adaptativo y Vulnerable**.

---

## 4. Seguridad, Privacidad y Resiliencia
- **Filtro PII (Privacy by Design):** Eliminación de nombres y documentos de identidad.
- **Modo Resiliente:** El generador de reportes ha sido programado para extraer evidencias textuales (citas) directamente del dataset en caso de fallos de red en la IA, garantizando que el documento de tesis siempre esté completo.

---
*Este documento es el sustento empírico de la tesis doctoral AMI-VIRTU.*
*Fecha: 27 de Abril de 2026 | Dataset N=295*
导导
