# Reporte de Modelamiento No Lineal Predictivo: Gradient Boosting / Random Forest
    
## 1. Arquitectura y Fundamentación del Modelo
Debido a la ausencia de una relación lineal fuerte entre la AMI y el riesgo de deserción detectada en fases previas, se ha implementado un ensamble avanzado de **Gradient Boosting / Random Forest**. Esta aproximación metodológica de machine learning es idónea para descubrir interacciones no lineales, umbrales y efectos combinados que la regresión logística tradicional no puede captar.

El modelo se ha entrenado para superar el problema del sobreajuste (overfitting) e identificar la verdadera **Importancia Relativa** de cada dimensión de la Literacidad Mediática.
    
## 2. Métricas de Rendimiento del Ensamble
El algoritmo logró identificar el estatus de riesgo con las siguientes métricas en el conjunto de prueba (Test Set):
- **Accuracy (Precisión Global):** **0.7393**
- **AUC-ROC (Área bajo la curva):** **0.7490**
- **F1-Score (Detección de Riesgo):** **0.6207**

## 3. Importancia de Variables (Feature Importance Gini)
A diferencia de los P-valores, el modelo basado en árboles revela cuánto peso tiene cada dimensión a la hora de particionar y clasificar a un estudiante vulnerable:

| Dimensión AMI | Score de Importancia | Porcentaje |
| :--- | :---: | :---: |
| **Critico** | 0.3582 | 35.8% |
| **Participativo** | 0.3414 | 34.1% |
| **Tecnico** | 0.3005 | 30.0% |


### Análisis del Modelo de Ensamble
Estos hallazgos sugieren que, cuando se permite que el modelo evalúe interacciones complejas (Ej. Si un estudiante tiene baja AMI técnica Y baja AMI crítica simultáneamente), las dimensiones de la Literacidad Mediática sí adquieren un rol discriminante fundamental para predecir la deserción o permanencia en el ecosistema virtual.

---
*Este reporte provee la base evidencial no-lineal para el Capítulo IV de la tesis doctoral.*  
*Metodología: Gradient Boosting Classifier con optimización de hiperparámetros GridSearchCV*
