# Reporte de Explicabilidad mediante IA (XAI): Análisis Axiomático SHAP

## 1. Fundamentación Ética de la IA Transparente
En una investigación de nivel doctoral, la capacidad predictiva de un algoritmo de Machine Learning debe estar obligatoriamente acompañada de su **explicabilidad**. Este reporte utiliza la técnica **SHAP (Shapley Additive Explanations)** para transformar nuestro modelo de predicción de riesgo en una herramienta de diagnóstico transparente.

## 2. Ranking de Impacto Macroscópico (Dimensiones)
El análisis SHAP sobre la cohorte evalúa la contribución marginal de cada variable predictora. El motor XAI permite identificar la importancia relativa de cada factor en la determinación del riesgo.

## 3. Microscopía del Riesgo: Análisis de Ítems Individuales
Gracias al motor XAI, hemos podido descender del nivel de "dimensiones" al nivel de **preguntas individuales** del cuestionario. Identificamos el Top 10 de ítems que más impacto tienen en la predicción del riesgo:

| Ranking | Ítem | Impacto SHAP (Abs) | Significado Pedagógico |
| :--- | :--- | :---: | :--- |
| **1°** | P5 | 0.2011 | Contribución a la predicción de riesgo |
| **2°** | P9 | 0.1256 | Contribución a la predicción de riesgo |
| **3°** | T4 | 0.1207 | Contribución a la predicción de riesgo |
| **4°** | C8 | 0.1131 | Contribución a la predicción de riesgo |
| **5°** | T6 | 0.1126 | Uso y manejo de herramientas del campus |
| **6°** | T9 | 0.1072 | Contribución a la predicción de riesgo |
| **7°** | T10 | 0.1038 | Contribución a la predicción de riesgo |
| **8°** | T7 | 0.0737 | Contribución a la predicción de riesgo |
| **9°** | T1 | 0.0671 | Contribución a la predicción de riesgo |
| **10°** | P10 | 0.0614 | Participación y comunicación colaborativa |


---
*Este análisis garantiza que las alertas tempranas del sistema son auditables y éticamente defendibles.*
