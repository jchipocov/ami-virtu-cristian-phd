# VADEMECUM ESTADÍSTICO - PROYECTO AMI-VIRTU & ARD-VIRTU (Alineación Tesis v2.0)

Este documento es el repositorio de criterios técnicos y conceptuales de la investigación. Toda la analítica se ejecuta bajo una arquitectura de **métodos mixtos secuenciales**, procesados exclusivamente en **Python 3.11**.

---

## 1. Definición del Constructo: Riesgo de Deserción
El riesgo se operacionaliza como una **variable dicotómica (Riesgo / No Riesgo)**, calculada mediante el orquestador `main.py` bajo los siguientes criterios de interrupción académica:
- **A1:** Interrupción de estudios (Boolean).
- **A2:** Número de desaprobados > 0.
- **A3:** Número de retiros > 0.
- **L2:** Inactividad en LMS > 15 días.
- *Umbral de Riesgo:* Si cualquiera de estas condiciones se cumple, el sujeto se etiqueta como **Riesgo_Total = 1**.

## 2. Fiabilidad de Instrumentos: AMI-VIRTU
Para garantizar la validez psicométrica sobre la muestra de **N=295**, se emplean:
- **Alfa de Cronbach ($\alpha$):** Consistencia interna clásica.
- **Omega de McDonald ($\omega$):** Estimador de alta precisión que asume cargas factoriales desiguales.
- **Manejo de Ítems Inversos:** Los ítems negativos (C6, T6, P5) se decodifican automáticamente para evitar sesgos en el cálculo.

## 3. Análisis Bivariado y Asociaciones
Se emplean coeficientes de asociación AMI vs Riesgo:
- **Pearson / Punto-Biserial:** Fuerza de la relación lineal.
- **Spearman:** Validación no paramétrica para distribuciones no normales.

## 4. Inferencia Predictiva: Regresión Logística
Se utiliza **Regresión Logística Binaria** mediante `statsmodels` para estimar el peso de las dimensiones AMI en la probabilidad de deserción.
- **Odds Ratios (OR):** Magnitud del cambio en la probabilidad. (Ej. OR=0.39 implica un factor protector del 61%).
- **Efectos de Interacción:** Se testea el impacto moderador del sentimiento académico sobre la relación AMI-Riesgo.

## 5. Segmentación por Perfiles (Ensamble Clustering)
Identificación de arquetipos pedagógicos mediante el cruce de 4 algoritmos:
1. **K-Means / Ward:** Estructura geométrica y varianza.
2. **GMM (Gaussian Mixture Models):** Densidad probabilística (validación de estabilidad).
3. **DBSCAN:** Identificación de casos atípicos (outliers).

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

---
*Este proyecto cumple estrictamente con el rigor metodológico para defensa de tesis doctoral.*
*Última Actualización: 27 de Abril de 2026*
导导
