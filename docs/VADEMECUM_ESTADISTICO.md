# VADEMECUM ESTADÍSTICO - PROYECTO AMI-VIRTU & ARD-VIRTU (Alineación Tesis v2.0)

Este documento es el repositorio de criterios técnicos y conceptuales de la investigación. Toda la analítica se ejecuta bajo una arquitectura de **métodos mixtos secuenciales**, procesados exclusivamente en **Python 3.11**.

---

## 1. Definición del Constructo: Riesgo de Deserción
El riesgo se operacionaliza como una variable multidimensional alineada con los **Objetivos 2 y 3** de la tesis, dividida en:
- **Dimensión Académica:** Basada en ítems **A1-A8** (Interrupción, desaprobación, retiros y autoeficacia académica).
- **Dimensión Comportamiento LMS:** Basada en ítems **L1-L8** (Frecuencia de acceso, puntualidad en entregas e inactividad).
- **Dimensión Continuidad:** Regla operativa que sintetiza el historial académico y la vinculación progresiva.
- *Umbral de Riesgo:* Se mantiene el cálculo de **Riesgo_Total = 1** (dicotómico) mediante una compuerta lógica OR para modelos predictivos, pero se analizan los puntajes continuos de cada sub-dimensión para el perfilamiento.

## 2. Fiabilidad y Validez Estructural
Para garantizar la validez psicométrica se emplean:
- **Alfa de Cronbach ($\alpha$) y Omega de McDonald ($\omega$):** Consistencia interna.
- **Prueba KMO (Kaiser-Meyer-Olkin):** Adecuación muestral (Umbral > 0.7).
- **Prueba de Esfericidad de Bartlett:** Significancia de la matriz de correlaciones ($p < 0.05$).
- **Manejo de Ítems Inversos:** Decodificación automática (C6, T6, P5).

## 3. Análisis Bivariado y Asociaciones Multidimensionales
Se emplean coeficientes de asociación AMI vs Riesgo bajo una matriz cruzada (3x3):
- **AMI (Crítica, Técnica, Participativa) vs RIESGO (Académica, LMS, Continuidad).**
- **Pearson / Punto-Biserial:** Fuerza de la relación lineal entre dimensiones.
- **Spearman:** Validación no paramétrica para detectar relaciones monótonas no lineales entre niveles AMI y severidad de riesgo.

## 4. Inferencia Predictiva: Regresión Logística
Se estima el peso de las dimensiones AMI en la probabilidad de deserción:
- **Odds Ratios (OR):** Magnitud del cambio en la probabilidad con IC 95%.
- **VIF (Variance Inflation Factor):** Detección de multicolinealidad (Umbral < 5).
- **Prueba de Hosmer-Lemeshow:** Bondad de ajuste del modelo (p > 0.05).
- **Pseudo R² de McFadden:** Medida de la varianza explicada por el modelo logit.

## 5. Segmentación y Consenso (Ensamble Clustering)
Identificación de arquetipos mediante 4 algoritmos:
- **K-Means / Ward / GMM / DBSCAN.**
- **Silhouette Score:** Cohesión y separación de los clústeres.
- **BIC (Bayesian Information Criterion):** Selección del número óptimo de grupos en GMM.
- **Adjusted Rand Index (ARI):** Medida de consenso y estabilidad entre diferentes algoritmos.

## 6. Inteligencia Artificial Explicable (XAI): SHAP
Uso de **KernelSHAP** para descomponer la importancia de los 30 ítems individuales. Esto permite identificar qué preguntas del test (ej. T6: Gestión de Plataformas) son los mayores detonantes de riesgo, dotando al modelo de transparencia ética.

## 7. Triangulación de Métodos Mixtos (FASE 11)
El modelo integra la "Voz del Estudiante" mediante:
- **Análisis de Sentimiento:** Procesamiento de lenguaje natural (NLP) de las respuestas abiertas.
- **Cruce de Alineación:** Identificación de disonancias entre el puntaje numérico y la expresión narrativa para detectar "riesgos invisibles".

## 8. Síntesis Narrativa Resiliente (FASE 12)
El motor de reportes está diseñado para operar en modo persistente:
- **Fase de IA:** Generación agéntica de conclusiones basadas en hallazgos estadísticos.
- **Fase de Evidencias:** Extracción automática de citas textuales de los alumnos para sustentar los reportes de clúster, garantizando la validez cualitativa incluso ante restricciones de cuota API.

## 9. Integridad y Reproducibilidad
- **Semillas Fijas:** Uso de `random_state` para replicabilidad de resultados.
- **Hashing SHA-256:** Verificación de integridad del dataset antes de cada ejecución.
- **Auditoría de Entorno:** Registro de versiones de librerías (Sklearn, Statsmodels).

---
*Este proyecto cumple estrictamente con el rigor metodológico para defensa de tesis doctoral.*
*Última Actualización: 28 de Abril de 2026 (Ajuste por Desglose Dimensional de Riesgo y Diagnósticos de Rigor)*
导导
