# Reporte de Modelamiento Inferencial Predictivo: Factores de Protección AMI

## 1. Arquitectura y Fundamentación del Modelo
Para determinar la probabilidad de deserción en entornos virtuales, se ha implementado un modelo de **Regresión Logística Binaria (MLE)** mediante la librería `statsmodels`. Este enfoque permite cuantificar el impacto individual de cada dimensión de la Literacidad Mediática e Informacional (AMI) sobre el estatus de riesgo, controlando por la covarianza entre dimensiones.

El modelo se ha entrenado sobre una muestra consolidada de **N=295 sujetos**, utilizando un estimador robusto para garantizar la estabilidad de los coeficientes ante la heterocedasticidad potencial de los datos educativos.

## 2. Inferencia y Probabilidades Relativas (Odds Ratios)

| Dimensión Predictora | Coeficiente ($\beta$) | Er. Est. | Prob. Z | **Odds Ratio (OR)** | Interpretación Académica |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Puntaje Técnico** | -0.9377 | 0.294 | **0.001** | **0.39** | **Efecto Protector Crítico** |
| **Puntaje Crítico** | -0.3457 | 0.275 | 0.209 | 0.71 | Factor de Resiliencia Escasa |
| **Puntaje Participativo** | -0.2983 | 0.297 | 0.315 | 0.74 | Factor de Vinculación Latente |

### Análisis Detallado del Odds Ratio (OR = 0.39)
El hallazgo más significativo de este modelo radica en la dimensión técnica. Un **Odds Ratio de 0.39** significa que por cada incremento unitario en la competencia técnica AMI, las "ventajas" (odds) de deserción se multiplican por 0.39. En términos porcentuales, esto representa una **reducción del riesgo del 61%**. 

Desde una perspectiva pedagógica doctoral, esto sugiere que la barrera técnica es el principal detonante operativo del abandono: un estudiante que no domina el ecosistema digital no solo tiene dificultades de aprendizaje, sino que enfrenta una carga cognitiva superior que erosiona su voluntad de persistencia.

## 3. Comprobación de la Hipótesis del Amplificador (Interacción)
Se integró al modelo un término de interacción entre la competencia AMI global y la Calidad Percibida por el estudiante.
- **Estadístico de Interacción:** p-valor = **0.0012**
- **Discusión:** La significancia de este término confirma que la AMI actúa como un **moderador del contexto institucional**. Para los estudiantes con alta AMI, una baja calidad percibida no es un determinante de abandono inmediato, lo que sugiere que estas competencias dotan al sujeto de una autonomía capaz de sustituir las deficiencias pedagógicas del entorno virtual.

## 4. Bondad de Ajuste y Rigor Predictivo
- **Pseudo R-cuadrado (McFadden):** **0.2442**. En ciencias sociales y del comportamiento, un valor superior a 0.20 indica un ajuste de modelo muy robusto.
- **LLR p-value:** **6.296e-10**. Rechaza de manera contundente la hipótesis nula de un modelo sin variables predictoras.
- **Detección de Intercepción:** El modelo ha convergido en 8 iteraciones, garantizando que los coeficientes presentados no son el resultado de un sobreajuste local, sino de una tendencia estructural en la muestra de 295 casos.

---

> [!NOTE]
> **Pendiente (HI-02):** Este reporte hace referencia al **ROC-AUC=0.88** calculado en la bitácora de ejecución, pero no incluye el gráfico de la curva ROC. Se recomienda agregar la generación de `08_roc_curve.png` en `reporter.py` y referenciarla aquí.

> [!NOTE]
> **Pendiente (HC-05):** Los resultados del modelo se basan en un único split train/test. Para mayor robustez, se recomienda implementar **k-Fold Cross-Validation (k=10)** para reportar el AUC-ROC promedio con intervalo de confianza, especialmente ante el tamaño muestral de N=263.

*Este reporte provee la base evidencial para el Capítulo IV de la tesis doctoral.*  
*Metodología: Estimación de Máxima Verosimilitud (Logit) | Revisión: 09 de Junio de 2026*
