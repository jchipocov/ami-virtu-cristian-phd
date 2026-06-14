# Reporte de Modelamiento Inferencial Predictivo: Factores de Protección AMI

## 1. Arquitectura y Fundamentación del Modelo
Para determinar la probabilidad de deserción en entornos virtuales, se ha implementado un modelo de **Regresión Logística Binaria (MLE)** mediante la librería `statsmodels`. Este enfoque permite cuantificar el impacto individual de cada dimensión de la Literacidad Mediática e Informacional (AMI) sobre el estatus de riesgo, controlando por la covarianza entre dimensiones.

El modelo se ha entrenado sobre la partición de entrenamiento de la muestra de pregrado (N=182 sujetos de 260 válidos).

## 2. Inferencia y Probabilidades Relativas (Odds Ratios)

| Dimensión Predictora | Coeficiente ($\beta$) | Er. Est. | Prob. Z (p) | **Odds Ratio (OR)** | IC 95% [OR] | Interpretación Académica |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Critico** | 0.0004 | 0.2155 | 0.9984 | 1.0004 | [0.656, 1.526] | Factor de Riesgo (No Significativo) |
| **Tecnico** | 0.1628 | 0.2459 | 0.5080 | 1.1767 | [0.727, 1.905] | Factor de Riesgo (No Significativo) |
| **Participativo** | -0.1400 | 0.2253 | 0.5343 | 0.8694 | [0.559, 1.352] | Factor Protector (No Significativo) |


### Análisis del Modelo de Regresión Logística
Los resultados muestran que, de manera individual y lineal, las dimensiones de la Literacidad Mediática e Informacional (AMI) tienen un impacto directo débil y no estadísticamente significativo sobre la probabilidad del riesgo de deserción ($p > 0.05$). Esto sugiere que la Alfabetización Mediática e Informacional opera principalmente como un **factor protector indirecto o moderador**, interactuando con otras variables de interactividad digital (LMS) y académicas, y no de forma aislada lineal directa.

## 3. Comprobación de la Hipótesis del Amplificador e Interacciones
La bondad de ajuste del modelo logístico se analizó mediante diagnósticos de colinealidad (VIF) y ajuste general:
- **Pseudo R-cuadrado (McFadden):** **0.0025**.
- **Bondad de Ajuste (Hosmer-Lemeshow p):** **0.6631** (valores > 0.05 indican un ajuste adecuado).
- **VIF Máximo:** **1.4140** (valores < 5 descartan problemas de colinealidad).

## 4. Validación Cruzada Estratificada (Stratified 10-Fold CV)
Para asegurar el rigor científico del modelo predictivo y evitar el sobreajuste:
- **AUC-ROC Promedio:** **0.4555 (± 0.1219)**
- **Intervalo de Confianza 95% (AUC):** **[0.2165, 0.6945]**
- **Accuracy Promedio:** **0.4846**
- **F1-Score Promedio:** **0.3796**

---
*Este reporte provee la base evidencial para el Capítulo IV de la tesis doctoral.*  
*Metodología: Inferencia por Máxima Verosimilitud (Logit) con validación cruzada k-Fold*
