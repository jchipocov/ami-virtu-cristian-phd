# Reporte de Explicabilidad mediante IA (XAI): Análisis Axiomático SHAP

## 1. Fundamentación Ética de la IA Transparente
En una investigación de nivel doctoral, la capacidad predictiva de un algoritmo de Machine Learning debe estar obligatoriamente acompañada de su **explicabilidad**. Este reporte utiliza la técnica **SHAP (Shapley Additive Explanations)** para transformar nuestro modelo de predicción de riesgo en una herramienta de diagnóstico transparente.

## 2. Ranking de Impacto Macroscópico (Dimensiones)
El análisis SHAP sobre la cohorte evalúa la contribución marginal de cada variable predictora. El motor XAI permite identificar la importancia relativa de cada factor en la determinación del riesgo.

## 3. Microscopía del Riesgo: Análisis de Ítems Individuales
Gracias al motor XAI, hemos podido descender del nivel de "dimensiones" al nivel de **preguntas individuales** del cuestionario. Identificamos el Top 10 de ítems que más impacto tienen en la predicción del riesgo:

| Ranking | Ítem | Impacto SHAP (Abs) | Significado Pedagógico |
| :--- | :--- | :---: | :--- |
| **1°** | C10 | 0.2825 | Capacidad crítica de evaluar información |
| **2°** | P10 | 0.2363 | Participación y comunicación colaborativa |
| **3°** | P3 | 0.2267 | Uso de canales digitales de participación |


---
*Este análisis garantiza que las alertas tempranas del sistema son auditables y éticamente defendibles.*
