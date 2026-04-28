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

### 2.2. Matriz Multidimensional de Riesgo (ARD-VIRTU)
El constructo "Riesgo de Deserción" se desglosa en tres dimensiones para el análisis de perfiles y correlaciones:
1.  **Dimensión Académica:** ítems `A1-A8`. Incluye interrupción de matrícula, créditos desaprobados, retiros y percepción de autoeficacia académica.
2.  **Dimensión Comportamiento LMS:** ítems `L1-L8`. Incluye frecuencia de acceso, inactividad prolongada y puntualidad en entregas.
3.  **Dimensión Continuidad:** Variable de síntesis que integra el historial de interrupción y desvinculación progresiva.

#### A. Algoritmo de Identificación de Riesgo Global
Para los modelos predictivos, se activa el riesgo ($Y=1$) si se cumple cualquier criterio de la compuerta lógica `OR` (ej. Inactividad > 15 días o Desaprobación >= 2 cursos). Sin embargo, el análisis descriptivo y de clústeres utiliza los **puntajes promediados** por dimensión para capturar la naturaleza específica de la vulnerabilidad.

#### B. El Detector de Inconsistencia y Ocultamiento
El módulo `DataCleaner` integra un **Detector de Inconsistencias** que genera una bandera estadística (`Flag_Inconsistencia = True`) sobre casos que mienten o responden al azar (ej. marcan 5 en todos los ítems AMI, ignorando los invertidos). En los modelos finales, estos registros son penalizados o excluidos mediante el **Filtro de Coherencia Agresivo (Indice < 0.6)**, asegurando que la tesis trabaje solo con "data limpia".

---

## 3. Plan Analítico Doctoral Multi-Fase

### Fase 1: Análisis Psicométrico y Validez Estructural
Se emplean estimadores de alta precisión para validar ambos instrumentos (AMI-VIRTU y ARD-VIRTU):
- **Alfa de Cronbach ($\alpha$) y Omega de McDonald ($\omega$):** Consistencia interna.
- **Prueba KMO (Kaiser-Meyer-Olkin):** Valida si los datos son aptos para el análisis factorial (Standard doctoral: > 0.70).
- **Prueba de Bartlett:** Asegura que la matriz de correlación no sea una matriz identidad ($p < 0.05$).

### Fase 2: Inferencia Predictiva y Diagnósticos de Rigor
Se utiliza el método de **Máxima Verosimilitud (MLE)** en `statsmodels` con los siguientes controles:
- **Odds Ratios (OR):** Interpretación probabilística con IC 95%.
- **Multicolinealidad (VIF):** Verificación de independencia entre dimensiones (VIF < 5).
- **Bondad de Ajuste (Hosmer-Lemeshow):** Validación del ajuste del modelo a los datos observados ($p > 0.05$).
- **McFadden R-squared:** Medición del poder explicativo del modelo de regresión.

### Fase 3: Inteligencia Artificial Explicable (XAI)
Uso de **KernelSHAP** para romper con el modelo de "caja negra":
- Se extrae un ranking de los 30 ítems individuales según su impacto real en el riesgo.
- Se identifican "Ítems Críticos" para la intervención pedagógica inmediata.

### Fase 4: Triangulación de Métodos Mixtos (Novedad Doctoral)
Se implementa una integración cuali-cuanti:
- **NLP de Sentimientos:** Procesamiento de las respuestas de la `Section B`.
- **Cruce de Disonancia:** Identificación de alumnos con alto AMI pero bajo sentimiento, permitiendo una detección proactiva de fatiga académica (burnout).

### Fase 5: Ensamble de Clustering y Estabilidad
Segmentación mediante 4 algoritmos: **K-Means, Ward, DBSCAN y GMM**.
- **Silhouette Score:** Evaluación de la calidad de la segmentación.
- **BIC Score:** Selección óptima de componentes en GMM.
- **Adjusted Rand Index (ARI):** Cuantificación del consenso entre los diferentes métodos de agrupamiento para garantizar la estabilidad del perfilamiento.

---

## 4. Seguridad, Privacidad y Resiliencia
- **Filtro PII (Privacy by Design):** Eliminación de nombres y documentos de identidad.
- **Integridad SHA-256:** El pipeline verifica el hash del dataset para asegurar que no ha habido alteraciones accidentales en la data de campo entre ejecuciones.
- **Modo Resiliente:** Extracción de evidencias textuales directa del dataset ante fallos de API.

---
*Este documento es el sustento empírico de la tesis doctoral AMI-VIRTU.*
*Fecha: 28 de Abril de 2026 | Dataset N=295 (Alineación Objetivos 2 y 3)*
导导
